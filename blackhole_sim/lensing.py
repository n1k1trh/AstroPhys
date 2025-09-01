from __future__ import annotations
import math
from dataclasses import dataclass
from .constants import schwarzschild_radius, G, c, PI
from .utils import Vec3

@dataclass
class Camera:
    pos: Vec3
    look: Vec3
    right: Vec3
    up: Vec3
    fov_rad: float

def default_camera(cam_distance: float, fov_deg: float) -> Camera:
    look = Vec3(0,0,-1).normalized()
    right = Vec3(1,0,0).normalized()
    up = Vec3(0,1,0).normalized()
    return Camera(pos=Vec3(0,0,cam_distance), look=look, right=right, up=up, fov_rad=math.radians(fov_deg))

def critical_impact_param(M: float) -> float:
    # b_c = 3*sqrt(3) GM/c^2
    return 3.0 * math.sqrt(3.0) * G * M / (c*c)

def meters_per_pixel(cam_distance: float, fov_rad: float, width: int) -> float:
    # small-angle: span = 2 * d * tan(fov/2)
    return (2.0 * cam_distance * math.tan(0.5*fov_rad)) / width
