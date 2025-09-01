from __future__ import annotations
import os, argparse
from typing import List
from .utils import RNG, write_png
from .physics import init_star_disk, step_newtonian, step_paczynski_wiita
from .render import render_particles, render_level3
from .scenes import default_scene

def run_level1(frames: int, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    scn = default_scene()
    rng = RNG()
    bodies = init_star_disk(scn, rng)
    for f in range(frames):
        img = render_particles(scn, bodies, apply_lensing=False)
        write_png(os.path.join(outdir, f"frame_{f:04d}.png"), scn.width, scn.height, img)
        step_newtonian(bodies, scn)

def run_level2(frames: int, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    scn = default_scene()
    rng = RNG()
    bodies = init_star_disk(scn, rng)
    for f in range(frames):
        img = render_particles(scn, bodies, apply_lensing=True)
        write_png(os.path.join(outdir, f"frame_{f:04d}.png"), scn.width, scn.height, img)
        step_paczynski_wiita(bodies, scn)

def run_level3(frames: int, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    scn = default_scene()
    for f in range(frames):
        img = render_level3(scn)
        write_png(os.path.join(outdir, f"frame_{f:04d}.png"), scn.width, scn.height, img)

def main():
    p = argparse.ArgumentParser(description="Black Hole Simulator (3 levels)")
    p.add_argument("--level", type=int, default=1, choices=[1,2,3], help="1: Newtonian, 2: Paczynski-Wiita + lensing, 3: shadow+disk renderer")
    p.add_argument("--frames", type=int, default=100)
    p.add_argument("--out", type=str, default="out")
    args = p.parse_args()

    if args.level == 1:
        run_level1(args.frames, args.out)
    elif args.level == 2:
        run_level2(args.frames, args.out)
    else:
        run_level3(args.frames, args.out)

if __name__ == "__main__":
    main()
