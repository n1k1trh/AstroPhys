import math

# SI constants
G = 6.67430e-11       # m^3 kg^-1 s^-2
c = 299_792_458.0     # m s^-1
PI = math.pi
TAU = 2.0 * math.pi

def schwarzschild_radius(M: float) -> float:
    """r_s = 2GM/c^2"""
    return 2.0 * G * M / (c * c)
