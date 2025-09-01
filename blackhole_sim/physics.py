from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List
from .utils import Vec3
from .constants import G, c, schwarzschild_radius

@dataclass
class Body:
    pos: Vec3
    vel: Vec3
    mass: float

@dataclass
class Scene:
    M_bh: float
    softening: float
    dt: float
    N: int
    disk_R: float
    star_mass: float
    width: int
    height: int
    fov_deg: float
    cam_distance: float
    disk_incl_deg: float

def circular_speed(M: float, r: float) -> float:
    return math.sqrt(G*M/r)

def init_star_disk(scn: Scene, rng) -> List[Body]:
    bodies: List[Body] = []
    Rmin = 0.05 * scn.disk_R
    for _ in range(scn.N):
        # log-ish distribution
        u = rng.uniform()
        r = Rmin * (scn.disk_R/Rmin) ** u
        ang = rng.uniform(0.0, 2*math.pi)
        pos = Vec3(r*math.cos(ang), r*math.sin(ang), (rng.uniform()-0.5)*0.02*scn.disk_R)
        v = circular_speed(scn.M_bh, r)
        vel = Vec3(-v*math.sin(ang), v*math.cos(ang), 0.0)
        bodies.append(Body(pos, vel, scn.star_mass))
    return bodies

def _acc_newton(rvec: Vec3, M: float, eps: float) -> Vec3:
    r2 = rvec.dot(rvec) + eps*eps
    invr3 = 1.0 / (math.sqrt(r2) * r2)
    return rvec * (-G * M * invr3)

def step_newtonian(bodies: List[Body], scn: Scene):
    h = scn.dt
    # kick
    for b in bodies:
        a = _acc_newton(b.pos, scn.M_bh, scn.softening)
        b.vel = b.vel + a * (0.5*h)
    # drift
    for b in bodies:
        b.pos = b.pos + b.vel * h
    # kick
    for b in bodies:
        a = _acc_newton(b.pos, scn.M_bh, scn.softening)
        b.vel = b.vel + a * (0.5*h)

def _acc_pw(rvec: Vec3, M: float, eps: float) -> Vec3:
    rs = schwarzschild_radius(M)
    r = rvec.norm() + eps
    denom = max(r - rs, 1e-6*rs)
    a_mag = -G*M/(denom*denom)
    return rvec.normalized() * a_mag

def step_paczynski_wiita(bodies: List[Body], scn: Scene):
    h = scn.dt
    for b in bodies:
        a = _acc_pw(b.pos, scn.M_bh, scn.softening)
        b.vel = b.vel + a * (0.5*h)
    for b in bodies:
        b.pos = b.pos + b.vel * h
    for b in bodies:
        a = _acc_pw(b.pos, scn.M_bh, scn.softening)
        b.vel = b.vel + a * (0.5*h)

def weak_field_deflection(M: float, b: float) -> float:
    # alpha ~ 4GM / (c^2 b)
    return 4.0 * G * M / (c*c * b)
