import pygame
import numpy as np
import sys
import argparse
import random

# Simulation constants
WIDTH, HEIGHT = 1000, 800
G = 6.674e-3  # scaled gravitational constant
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 100)
BLUE = (100, 200, 255)

class Body:
    def __init__(self, x, y, mass, vx=0, vy=0, color=WHITE, radius=3):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([vx, vy], dtype=float)
        self.mass = mass
        self.color = color
        self.radius = radius

    def update(self, bodies, dt):
        force = np.zeros(2)
        for other in bodies:
            if other is self:
                continue
            r_vec = other.pos - self.pos
            r = np.linalg.norm(r_vec)
            if r > 2:  # avoid singularity
                f = G * self.mass * other.mass / (r*r)
                force += f * (r_vec / r)
        self.vel += (force / self.mass) * dt
        self.pos += self.vel * dt

    def draw(self, screen, camera):
        x, y = camera.world_to_screen(self.pos)
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

class Camera:
    def __init__(self):
        self.offset = np.array([WIDTH/2, HEIGHT/2], dtype=float)
        self.zoom = 1.0

    def world_to_screen(self, pos):
        return (pos * self.zoom + self.offset)

    def move(self, dx, dy):
        self.offset += np.array([dx, dy])

    def adjust_zoom(self, factor):
        self.zoom *= factor

def setup_level(level):
    bodies = []
    if level == 1:
        # Single black hole + orbiting stars
        bh = Body(WIDTH/2, HEIGHT/2, mass=1e6, color=YELLOW, radius=8)
        bodies.append(bh)
        for _ in range(20):
            angle = random.uniform(0, 2*np.pi)
            r = random.uniform(100, 300)
            x = WIDTH/2 + r*np.cos(angle)
            y = HEIGHT/2 + r*np.sin(angle)
            v = np.sqrt(G*bh.mass/r)
            vx, vy = -v*np.sin(angle), v*np.cos(angle)
            bodies.append(Body(x, y, 10, vx, vy, BLUE, 3))
    elif level == 2:
        # Binary black hole
        bh1 = Body(WIDTH/2 - 100, HEIGHT/2, mass=5e5, color=YELLOW, radius=7)
        bh2 = Body(WIDTH/2 + 100, HEIGHT/2, mass=5e5, color=YELLOW, radius=7)
        bodies += [bh1, bh2]
        for _ in range(30):
            x = random.uniform(200, 800)
            y = random.uniform(200, 600)
            vx, vy = random.uniform(-1, 1), random.uniform(-1, 1)
            bodies.append(Body(x, y, 5, vx, vy, BLUE, 3))
    elif level == 3:
        # Galaxy-like
        center = Body(WIDTH/2, HEIGHT/2, mass=2e6, color=YELLOW, radius=10)
        bodies.append(center)
        for _ in range(100):
            angle = random.uniform(0, 2*np.pi)
            r = random.uniform(50, 400)
            x = WIDTH/2 + r*np.cos(angle)
            y = HEIGHT/2 + r*np.sin(angle)
            v = np.sqrt(G*center.mass/r)
            vx, vy = -v*np.sin(angle), v*np.cos(angle)
            bodies.append(Body(x, y, 5, vx, vy, WHITE, 2))
    return bodies

def run(level):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Black Hole Simulation (Level {})".format(level))
    clock = pygame.time.Clock()
    camera = Camera()
    paused = False

    bodies = setup_level(level)

    running = True
    while running:
        dt = clock.tick(FPS) / 10.0  # slow down time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    camera.adjust_zoom(1.1)
                elif event.key == pygame.K_MINUS:
                    camera.adjust_zoom(0.9)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click adds star
                    mx, my = event.pos
                    world_pos = (np.array([mx, my]) - camera.offset) / camera.zoom
                    bodies.append(Body(world_pos[0], world_pos[1], 10, random.uniform(-1,1), random.uniform(-1,1), BLUE, 3))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: camera.move(10, 0)
        if keys[pygame.K_RIGHT]: camera.move(-10, 0)
        if keys[pygame.K_UP]: camera.move(0, 10)
        if keys[pygame.K_DOWN]: camera.move(0, -10)

        if not paused:
            for body in bodies:
                body.update(bodies, dt)

        screen.fill(BLACK)
        for body in bodies:
            body.draw(screen, camera)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", type=int, default=1, help="Simulation level (1, 2, or 3)")
    args = parser.parse_args()
    run(args.level)

