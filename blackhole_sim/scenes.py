from __future__ import annotations
from .physics import Scene
from .constants import schwarzschild_radius

def default_scene() -> Scene:
    # ~10 solar mass BH
    M_sun = 1.98847e30
    M_bh = 10.0 * M_sun
    rs = schwarzschild_radius(M_bh)
    return Scene(
        M_bh=M_bh,
        softening=0.5*rs,
        dt=0.02,                # seconds (sim time, arbitrary scale)
        N=1200,                 # star count
        disk_R=150.0*rs,        # initial disk size
        star_mass=1.0*M_sun,    # identical mass (not used in forces here)
        width=900, height=900,
        fov_deg=40.0,
        cam_distance=2000.0*rs,
        disk_incl_deg=60.0
    )
