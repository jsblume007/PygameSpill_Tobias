import pygame as pg
from constants import *
from dataclasses import dataclass
import math
import random

@dataclass
class Circle:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    px: float = 0.0
    py: float = 0.0
    r: int = 0


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def vec_length(x: float, y: float) -> float:
    return math.hypot(x, y)


def vec_normalize(x: float, y: float) -> tuple[float, float]:
    l = vec_length(x, y)
    return (x / l, y / l) if l != 0 else (0.0, 0.0)


def reset_puck(p: Circle) -> None:
    p.x = BREDDE / 2
    p.y = HOYDE / 2
    angle = random.uniform(-0.6, 0.6) + random.choice([0, math.pi])
    speed = 9.0
    p.vx = math.cos(angle) * speed
    p.vy = math.sin(angle) * speed


def keep_in_half(player: Circle, left_half: bool) -> None:
    player.x = clamp(player.x, MARGIN + player.r, BREDDE - MARGIN - player.r)
    player.y = clamp(player.y, MARGIN + player.r, HOYDE - MARGIN - player.r)

    if left_half:
        player.x = clamp(player.x, MARGIN + player.r, BREDDE / 2 - player.r)
    else:
        player.x = clamp(player.x, BREDDE / 2 + player.r, BREDDE - MARGIN - player.r)


def handle_collision(player: Circle, puck: Circle) -> None:
    dx = puck.x - player.x
    dy = puck.y - player.y
    dist = vec_length(dx, dy)
    min_dist = player.r + puck.r

    if dist >= min_dist:
        return

    nx, ny = vec_normalize(dx, dy)
    overlap = min_dist - dist
    puck.x += nx * overlap
    puck.y += ny * overlap

    rvx = puck.vx - player.vx
    rvy = puck.vy - player.vy

    vn = rvx * nx + rvy * ny
    if vn > 0:
        return

    e = 1.05
    rvx -= (1 + e) * vn * nx
    rvy -= (1 + e) * vn * ny

    puck.vx = rvx + player.vx * 0.9
    puck.vy = rvy + player.vy * 0.9

    speed = vec_length(puck.vx, puck.vy)
    if speed > PUCK_MAKS_FART:
        scale = PUCK_MAKS_FART / speed
        puck.vx *= scale
        puck.vy *= scale


def handle_wall_collisions(puck: Circle) -> None:
    if puck.y - puck.r <= MARGIN:
        puck.y = MARGIN + puck.r
        puck.vy *= -SPRETT

    if puck.y + puck.r >= HOYDE - MARGIN:
        puck.y = HOYDE - MARGIN - puck.r
        puck.vy *= -SPRETT

    if puck.x - puck.r <= MARGIN:
        if not (MAL_Y1 <= puck.y <= MAL_Y2):
            puck.x = MARGIN + puck.r
            puck.vx *= -SPRETT

    if puck.x + puck.r >= BREDDE - MARGIN:
        if not (MAL_Y1 <= puck.y <= MAL_Y2):
            puck.x = BREDDE - MARGIN - puck.r
            puck.vx *= -SPRETT


def check_goal(puck: Circle) -> str | None:
    if puck.x + puck.r < MARGIN and (MAL_Y1 <= puck.y <= MAL_Y2):
        return "HOYRE"

    if puck.x - puck.r > BREDDE - MARGIN and (MAL_Y1 <= puck.y <= MAL_Y2):
        return "VENSTRE"

    return None


def main() -> None:
    pg.init()
    skjerm = pg.display.set_mode((BREDDE, HOYDE))
    pg.display.set_caption("Air Hockey (forenklet) - 2 spillere")
    klokke = pg.time.Clock()

    font = pg.font.SysFont("arial", 34, bold=True)
    liten = pg.font.SysFont("arial", 18)

    venstre = Circle(BREDDE * 0.25, HOYDE / 2, r=KOLLE_R)
    hoyre = Circle(BREDDE * 0.75, HOYDE / 2, r=KOLLE_R)
    puck = Circle(BREDDE / 2, HOYDE / 2, r=PUCK_R)

    poeng_v = 0
    poeng_h = 0

    reset_puck(puck)

    running = True
    while running:
        klokke.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            running = False

        venstre.px, venstre.py = venstre.x, venstre.y
        hoyre.px, hoyre.py = hoyre.x, hoyre.y

        vx = (keys[pg.K_d] - keys[pg.K_a])
        vy = (keys[pg.K_s] - keys[pg.K_w])

        hx = (keys[pg.K_RIGHT] - keys[pg.K_LEFT])
        hy = (keys[pg.K_DOWN] - keys[pg.K_UP])

        if vx != 0 or vy != 0:
            nx, ny = vec_normalize(vx, vy)
            venstre.x += nx * KOLLE_FART
            venstre.y += ny * KOLLE_FART

        if hx != 0 or hy != 0:
            nx, ny = vec_normalize(hx, hy)
            hoyre.x += nx * KOLLE_FART
            hoyre.y += ny * KOLLE_FART

        keep_in_half(venstre, left_half=True)
        keep_in_half(hoyre, left_half=False)

        venstre.vx = (venstre.x - venstre.px) * FPS
        venstre.vy = (venstre.y - venstre.py) * FPS

        hoyre.vx = (hoyre.x - hoyre.px) * FPS
        hoyre.vy = (hoyre.y - hoyre.py) * FPS

        puck.x += puck.vx
        puck.y += puck.vy

        puck.vx *= FRIKSJON
        puck.vy *= FRIKSJON

        handle_collision(venstre, puck)
        handle_collision(hoyre, puck)

        handle_wall_collisions(puck)

        mål = check_goal(puck)
        if mål == "VENSTRE":
            poeng_v += 1
            reset_puck(puck)
        elif mål == "HOYRE":
            poeng_h += 1
            reset_puck(puck)

        skjerm.fill(BAKGRUNN)

        pg.draw.rect(
            skjerm,
            HVIT,
            (MARGIN, MARGIN, BREDDE - 2 * MARGIN, HOYDE - 2 * MARGIN),
            3,
        )

        pg.draw.line(
            skjerm,
            HVIT,
            (BREDDE / 2, MARGIN),
            (BREDDE / 2, HOYDE - MARGIN),
            2,
        )

        pg.draw.circle(skjerm, HVIT, (int(BREDDE / 2), int(HOYDE / 2)), 70, 2)

        pg.draw.rect(skjerm, GUL, (0, MAL_Y1, MARGIN, MAL_HOYDE))
        pg.draw.rect(skjerm, GUL, (BREDDE - MARGIN, MAL_Y1, MARGIN, MAL_HOYDE))

        pg.draw.circle(skjerm, BLA, (int(venstre.x), int(venstre.y)), venstre.r)
        pg.draw.circle(skjerm, ROD, (int(hoyre.x), int(hoyre.y)), hoyre.r)
        pg.draw.circle(skjerm, HVIT, (int(puck.x), int(puck.y)), puck.r)

        tekst = font.render(f"{poeng_v}   -   {poeng_h}", True, HVIT)
        skjerm.blit(tekst, (BREDDE / 2 - tekst.get_width() / 2, 18))

        hjelp = liten.render("Venstre: WASD | Høyre: piltaster | ESC: avslutt", True, (220, 230, 235))
        skjerm.blit(hjelp, (BREDDE / 2 - hjelp.get_width() / 2, HOYDE - 28))

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()