import pygame as pg
import random
import math

# -------------------- innstillinger --------------------
BREDDE, HOYDE = 900, 500
FPS = 60

RADIUS_KOLLE = 25
RADIUS_PUCK = 14

FART_KOLLE = 6
FRIKSJON = 0.995
MAKS_FART_PUCK = 12

MAL_APNING = 160  # åpning midt på venstre/høyre vegg

HVIT = (240, 240, 240)
GRA = (130, 130, 130)
BLA = (80, 160, 255)
ROD = (255, 90, 90)
BAKGRUNN = (20, 24, 28)
GRONN = (100, 255, 160)

# -------------------- hjelpefunksjoner --------------------
def klem(x, lav, hoy):
    return max(lav, min(hoy, x))

def avstand(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

# -------------------- klasser --------------------
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

        # hold inne i brettet
        self.x = klem(self.x, RADIUS_KOLLE, BREDDE - RADIUS_KOLLE)
        self.y = klem(self.y, RADIUS_KOLLE, HOYDE - RADIUS_KOLLE)

        # hver sin halvdel
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

        # tilfeldig startfart
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

        # friksjon
        self.vx *= FRIKSJON
        self.vy *= FRIKSJON

        # maks fart
        fart = math.hypot(self.vx, self.vy)
        if fart > MAKS_FART_PUCK:
            self.vx = self.vx / fart * MAKS_FART_PUCK
            self.vy = self.vy / fart * MAKS_FART_PUCK

    def vegger_og_mal(self):
        # målåpning (midt på høyden)
        mal_topp = (HOYDE - MAL_APNING) / 2
        mal_bunn = (HOYDE + MAL_APNING) / 2

        # topp/bunn spretter alltid
        if self.y - RADIUS_PUCK <= 0:
            self.y = RADIUS_PUCK
            self.vy *= -1
        if self.y + RADIUS_PUCK >= HOYDE:
            self.y = HOYDE - RADIUS_PUCK
            self.vy *= -1

        # venstre vegg: enten mål eller sprett
        if self.x - RADIUS_PUCK <= 0:
            if mal_topp <= self.y <= mal_bunn:
                return "mal_venstre"
            self.x = RADIUS_PUCK
            self.vx *= -1

        # høyre vegg
        if self.x + RADIUS_PUCK >= BREDDE:
            if mal_topp <= self.y <= mal_bunn:
                return "mal_hoyre"
            self.x = BREDDE - RADIUS_PUCK
            self.vx *= -1

        return None

    def kollisjon_med_kolle(self, kolle: Kolle):
        # hvis pucken er nær kølla -> sprett
        d = avstand(self.x, self.y, kolle.x, kolle.y)
        if d < RADIUS_PUCK + RADIUS_KOLLE:
            # dytt pucken litt bort fra kølla (så den ikke "setter seg fast")
            dx = self.x - kolle.x
            dy = self.y - kolle.y

            # hvis dx,dy er 0, gi en liten retning
            if dx == 0 and dy == 0:
                dx = 1

            lengde = math.hypot(dx, dy)
            nx = dx / lengde
            ny = dy / lengde

            # flytt pucken ut
            self.x = kolle.x + nx * (RADIUS_PUCK + RADIUS_KOLLE)
            self.y = kolle.y + ny * (RADIUS_PUCK + RADIUS_KOLLE)

            # superenkel sprett: bare sett farten i normal-retningen
            fart = max(7, math.hypot(self.vx, self.vy) * 1.05)  # litt boost
            self.vx = nx * fart
            self.vy = ny * fart

    def tegn(self, skjerm):
        pg.draw.circle(skjerm, HVIT, (int(self.x), int(self.y)), RADIUS_PUCK)
        pg.draw.circle(skjerm, GRA, (int(self.x), int(self.y)), RADIUS_PUCK, 2)

# -------------------- tegn bane --------------------
def tegn_bane(skjerm, poeng_v, poeng_h, font):
    skjerm.fill(BAKGRUNN)

    # midtlinje
    pg.draw.line(skjerm, GRA, (BREDDE//2, 0), (BREDDE//2, HOYDE), 2)

    # mål
    mal_topp = int((HOYDE - MAL_APNING) / 2)
    mal_bunn = int((HOYDE + MAL_APNING) / 2)
    pg.draw.line(skjerm, GRONN, (0, mal_topp), (0, mal_bunn), 6)
    pg.draw.line(skjerm, GRONN, (BREDDE, mal_topp), (BREDDE, mal_bunn), 6)

    # score
    tekst = font.render(f"{poeng_v} - {poeng_h}", True, HVIT)
    skjerm.blit(tekst, (BREDDE//2 - tekst.get_width()//2, 10))

# -------------------- hovedprogram --------------------
def main():
    pg.init()
    skjerm = pg.display.set_mode((BREDDE, HOYDE))
    pg.display.set_caption("Airhockey (ENKEL) - 2 spillere")
    klokke = pg.time.Clock()
    font = pg.font.SysFont(None, 50)

    venstre = Kolle(200, HOYDE/2, BLA, venstre_side=True)
    hoyre = Kolle(BREDDE-200, HOYDE/2, ROD, venstre_side=False)
    puck = Puck()

    poeng_v = 0
    poeng_h = 0

    running = True
    while running:
        klokke.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        taster = pg.key.get_pressed()

        # flytt køller
        venstre.flytt(taster, pg.K_w, pg.K_s, pg.K_a, pg.K_d)
        hoyre.flytt(taster, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)

        # oppdater puck + kollisjon
        puck.oppdater()
        puck.kollisjon_med_kolle(venstre)
        puck.kollisjon_med_kolle(hoyre)

        # vegger og mål
        mal = puck.vegger_og_mal()
        if mal == "mal_venstre":
            poeng_h += 1
            puck.reset(retning="venstre")
        elif mal == "mal_hoyre":
            poeng_v += 1
            puck.reset(retning="hoyre")

        # tegn
        tegn_bane(skjerm, poeng_v, poeng_h, font)
        venstre.tegn(skjerm)
        hoyre.tegn(skjerm)
        puck.tegn(skjerm)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
