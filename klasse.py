import pygame as pg
import random
import math

from constants import *

class Kolle:
    def __init__(self, x, y, farge, venstre_side):
        self.x = x
        self.y = y
        self.farge = farge
        self.venstre_side = venstre_side

    def flytt(self, taster, opp, ned, venstre, hoyre):
        if taster[venstre]:
            self.x -= FART_KOLLE
        if taster[hoyre]:
            self.x += FART_KOLLE
        if taster[opp]:
            self.y -= FART_KOLLE
        if taster[ned]:
            self.y += FART_KOLLE

        self.x = klem(self.x, RADIUS_KOLLE, BREDDE - RADIUS_KOLLE)
        self.y = klem(self.y, RADIUS_KOLLE, HOYDE - RADIUS_KOLLE)

        midt = BREDDE // 2
        if self.venstre_side:
            self.x = klem(self.x, RADIUS_KOLLE, midt - RADIUS_KOLLE)
        else:
            self.x = klem(self.x, midt + RADIUS_KOLLE, BREDDE - RADIUS_KOLLE)

    def tegn(self, skjerm):
        pg.draw.circle(skjerm, self.farge, (int(self.x), int(self.y)), RADIUS_KOLLE)
        pg.draw.circle(skjerm, HVIT, (int(self.x), int(self.y)), RADIUS_KOLLE, 2)


class Puck:
    def __init__(self):
        self.reset()

    def reset(self, retning=None):
        self.x = BREDDE / 2
        self.y = HOYDE / 2

        vx = random.choice([-6, 6])
        vy = random.choice([-3, -2, -1, 1, 2, 3])

        if retning == "venstre":
            vx = -abs(vx)
        if retning == "hoyre":
            vx = abs(vx)

        self.vx = vx
        self.vy = vy

    def oppdater(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= FRIKSJON
        self.vy *= FRIKSJON

        fart = math.hypot(self.vx, self.vy)
        if fart > MAKS_FART_PUCK:
            self.vx = self.vx / fart * MAKS_FART_PUCK
            self.vy = self.vy / fart * MAKS_FART_PUCK

    def vegger_og_mal(self):
        mal_topp = (HOYDE - MAL_APNING) / 2
        mal_bunn = (HOYDE + MAL_APNING) / 2

        if self.y - RADIUS_PUCK <= 0:
            self.y = RADIUS_PUCK
            self.vy *= -1
        if self.y + RADIUS_PUCK >= HOYDE:
            self.y = HOYDE - RADIUS_PUCK
            self.vy *= -1

        if self.x - RADIUS_PUCK <= 0:
            if mal_topp <= self.y <= mal_bunn:
                return "mal_venstre"
            self.x = RADIUS_PUCK
            self.vx *= -1

        if self.x + RADIUS_PUCK >= BREDDE:
            if mal_topp <= self.y <= mal_bunn:
                return "mal_hoyre"
            self.x = BREDDE - RADIUS_PUCK
            self.vx *= -1

        return None

    def kollisjon_med_kolle(self, kolle: Kolle):
        d = avstand(self.x, self.y, kolle.x, kolle.y)
        if d < RADIUS_PUCK + RADIUS_KOLLE:
            dx = self.x - kolle.x
            dy = self.y - kolle.y

            if dx == 0 and dy == 0:
                dx = 1

            lengde = math.hypot(dx, dy)
            nx = dx / lengde
            ny = dy / lengde

            self.x = kolle.x + nx * (RADIUS_PUCK + RADIUS_KOLLE)
            self.y = kolle.y + ny * (RADIUS_PUCK + RADIUS_KOLLE)

            fart = max(7, math.hypot(self.vx, self.vy) * 1.05)
            self.vx = nx * fart
            self.vy = ny * fart

    def tegn(self, skjerm):
        pg.draw.circle(skjerm, HVIT, (int(self.x), int(self.y)), RADIUS_PUCK)
        pg.draw.circle(skjerm, GRA, (int(self.x), int(self.y)), RADIUS_PUCK, 2)
