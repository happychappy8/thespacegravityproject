"""VGA Trainer Part 13: a 3D starfield, in Python.

pip install pygame numpy     then     python part13.py
Space reverses direction, W toggles warp streaks. Esc quits.
"""
import pygame
import numpy as np


def vga_palette():
    """An approximation of the VGA BIOS default palette."""
    pal = [(0,0,0),(0,0,42),(0,42,0),(0,42,42),
           (42,0,0),(42,0,42),(42,21,0),(42,42,42),
           (21,21,21),(21,21,63),(21,63,21),(21,63,63),
           (63,21,21),(63,21,63),(63,63,21),(63,63,63)]
    pal += [(g, g, g) for g in (0, 5, 8, 11, 14, 17, 20, 24,
                                 28, 32, 36, 40, 45, 50, 56, 63)]
    for hi, lows in ((63, (0, 31, 45)), (28, (0, 14, 20)),
                     (16, (0, 8, 11))):
        for lo in lows:
            s = [round(lo + (hi - lo) * k / 4) for k in range(5)]
            pal += [(s[k], lo, hi) for k in range(4)]
            pal += [(hi, lo, s[4-k]) for k in range(4)]
            pal += [(hi, s[k], lo) for k in range(4)]
            pal += [(s[4-k], hi, lo) for k in range(4)]
            pal += [(lo, hi, s[k]) for k in range(4)]
            pal += [(lo, s[4-k], hi) for k in range(4)]
    pal += [(0, 0, 0)] * (256 - len(pal))
    return [tuple(round(v * 255 / 63) for v in c) for c in pal]

NUM = 400
rng = np.random.default_rng()


def new_stars(n, z):
    return (rng.uniform(-1000, 1000, n), rng.uniform(-1000, 1000, n),
            np.full(n, float(z)) if z else rng.uniform(1, 1000, n))


def main():
    pygame.init()
    screen = pygame.display.set_mode((320, 200), pygame.SCALED)
    pygame.display.set_caption("VGA Trainer: Part 13")
    vga = pygame.Surface((320, 200), 0, 8)
    vga.set_palette(vga_palette())
    xs, ys, zs = new_stars(NUM, None)
    speed, warp = 8, False
    clock = pygame.time.Clock()
    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    speed = -speed
                elif event.key == pygame.K_w:
                    warp = not warp
        pixels = pygame.surfarray.pixels2d(vga)
        if warp:
            lit = pixels > 16
            pixels[lit] -= 1
        else:
            pixels[:] = 0
        zs -= speed
        sx = np.round(xs * 128 / zs + 160).astype(int)
        sy = np.round(ys * 128 / zs + 100).astype(int)
        gone = (zs < 1) | (zs > 1000) | (sx < 0) | (sx > 319) | (sy < 0) | (sy > 199)
        if gone.any():
            nx, ny, nz = new_stars(gone.sum(), 1000 if speed > 0 else 50)
            xs[gone], ys[gone], zs[gone] = nx, ny, nz
        ok = ~gone
        pixels[sx[ok], sy[ok]] = np.clip(31 - (zs[ok] // 67).astype(int), 16, 31)
        del pixels
        screen.blit(vga, (0, 0))
        pygame.display.flip()
        t += 1
        clock.tick(70)
    pygame.quit()


if __name__ == "__main__":
    main()