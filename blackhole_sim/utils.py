from __future__ import annotations
import math, random
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image

@dataclass
class Vec3:
    x: float
    y: float
    z: float = 0.0
    def __add__(self,o): return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self,o): return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self,s: float): return Vec3(self.x*s, self.y*s, self.z*s)
    __rmul__ = __mul__
    def __truediv__(self,s: float): return Vec3(self.x/s, self.y/s, self.z/s)
    def dot(self,o): return self.x*o.x + self.y*o.y + self.z*o.z
    def norm(self): return math.sqrt(self.dot(self))
    def normalized(self):
        n=self.norm()
        return self if n==0 else self/n

def clamp(x,a,b): return a if x<a else b if x>b else x

class RNG:
    def __init__(self, seed: int | None=None):
        self.r = random.Random(seed)
    def uniform(self,a=0.0,b=1.0): return self.r.uniform(a,b)
    def randint(self,a,b): return self.r.randint(a,b)
    def normal(self,mu=0.0,sigma=1.0): 
        # Box-Muller
        u1 = self.r.random()+1e-12; u2 = self.r.random()+1e-12
        z = math.sqrt(-2.0*math.log(u1))*math.cos(2*math.pi*u2)
        return mu + sigma*z

def write_png(path: str, W: int, H: int, pixels: List[Tuple[int,int,int]]):
    img = Image.new("RGB", (W,H))
    img.putdata(pixels)
    img.save(path)
