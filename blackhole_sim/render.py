from __future__ import annotations
import math
from typing import List, Tuple
from .utils import Vec3, clamp
from .constants import schwarzschild_radius, G, c, PI
from .physics import Body, Scene, weak_field_deflection
from .lensing import default_camera, critical_impact_param, meters_per_pixel

RGB = Tuple[int,int,int]

def _plot_disk_and_shadow(scn: Scene) -> List[RGB]:
    W,H = scn.width, scn.height
    pixels: List[RGB] = [(0,0,0)] * (W*H)

    # Background starfield (random speckles)
    import random
    rnd = random.Random(42)
    for _ in range(4000):
        x = rnd.randrange(0, W); y = rnd.randrange(0, H)
        s = 200 + rnd.randrange(0, 55)
        idx = y*W + x
        pixels[idx] = (s,s,s)

    # Shadow radius in pixels
    bc = critical_impact_param(scn.M_bh)
    mpp = meters_per_pixel(scn.cam_distance, math.radians(scn.fov_deg), W)
    px_per_m = 1.0 / mpp
    cx, cy = W//2, H//2
    Rshadow = max(2, int(round(bc * px_per_m)))

    # Draw the shadow (filled)
    for y in range(cy-Rshadow-2, cy+Rshadow+3):
        if y<0 or y>=H: continue
        dy = y - cy
        span = int((Rshadow*Rshadow - dy*dy)**0.5) if abs(dy)<=Rshadow else -1
        if span>=0:
            for x in range(cx-span, cx+span+1):
                if 0<=x<W:
                    pixels[y*W+x]=(0,0,0)

    # Thin disk from r_isco=3r_s to r_outer
    rs = schwarzschild_radius(scn.M_bh)
    r_isco = 3.0 * rs
    r_outer = 30.0 * rs
    inc = math.radians(scn.disk_incl_deg)

    r = r_isco
    dr = 0.5*rs
    while r <= r_outer:
        v = (G*scn.M_bh / r) ** 0.5
        beta = v / c
        gamma = 1.0 / (1.0 - beta*beta) ** 0.5
        steps = max(180, min(2000, int(2*math.pi*r/dr)))
        for i in range(steps):
            th = (i/steps) * 2.0*math.pi
            X = r*math.cos(th)
            Y = r*math.sin(th)*math.cos(inc)
            # project
            x = cx + int(round(X * px_per_m))
            y = cy - int(round(Y * px_per_m))
            if 0<=x<W and 0<=y<H:
                cos_t = math.sin(th)*math.sin(inc)
                boost = (gamma * (1.0 - beta * cos_t)) ** -3.0
                emiss = 1.0 / (r*r)
                b = 3e6 * emiss * boost
                b = clamp(b, 0.0, 255.0)
                val = int(b)
                # warm tint in the approaching side
                pixels[y*W+x] = (min(255, val+40), val, int(0.7*val))
        r += dr

    return pixels

def render_level3(scn: Scene) -> List[RGB]:
    return _plot_disk_and_shadow(scn)

def render_particles(scn: Scene, bodies: List[Body], apply_lensing: bool=False) -> List[RGB]:
    W,H = scn.width, scn.height
    pixels: List[RGB] = [(0,0,0)] * (W*H)
    cx, cy = W//2, H//2
    # scale so that disk_R fits well
    scale = 0.45 * min(W,H) / scn.disk_R

    # draw BH shadow outline
    bc = critical_impact_param(scn.M_bh)
    mpp = meters_per_pixel(scn.cam_distance, math.radians(scn.fov_deg), W)
    px_per_m = 1.0 / mpp
    Rshadow = max(1, int(round(bc * px_per_m)))
    for t in range(360):
        x = cx + int(round(Rshadow * math.cos(math.radians(t))))
        y = cy + int(round(Rshadow * math.sin(math.radians(t))))
        if 0<=x<W and 0<=y<H: pixels[y*W+x]=(5,5,5)

    # draw stars
    for b in bodies:
        x = cx + int(round(b.pos.x * scale))
        y = cy - int(round(b.pos.y * scale))
        # weak-field lensing shift (small) by deflection alpha, approximate mapping
        if apply_lensing:
            b_perp = max(1e-6, (b.pos.x*b.pos.x + b.pos.y*b.pos.y) ** 0.5)
            alpha = weak_field_deflection(scn.M_bh, b_perp)
            # pixel shift ~ alpha * focal_length_pixels (small-angle)
            fpx = (W/2) / math.tan(0.5*math.radians(scn.fov_deg))
            shift = alpha * fpx
            # shift radially toward the BH
            rx = b.pos.x / b_perp; ry = b.pos.y / b_perp
            x -= int(round(shift * rx * 0.2))  # scale down to avoid over-shift
            y += int(round(shift * ry * 0.2))

        for dy in (-1,0,1):
            for dx in (-1,0,1):
                xx, yy = x+dx, y+dy
                if 0<=xx<W and 0<=yy<H:
                    pixels[yy*W+xx] = (255,255,200)
    return pixels
