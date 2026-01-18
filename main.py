import pygame as pg
from constants import *
from klasse import *

def tegn_bane(skjerm, poeng_v, poeng_h, font):
    skjerm.fill(BAKGRUNN)

    pg.draw.line(skjerm, GRA, (BREDDE//2, 0), (BREDDE//2, HOYDE), 2)

    mal_topp = int((HOYDE - MAL_APNING) / 2)
    mal_bunn = int((HOYDE + MAL_APNING) / 2)
    pg.draw.line(skjerm, GRONN, (0, mal_topp), (0, mal_bunn), 6)
    pg.draw.line(skjerm, GRONN, (BREDDE, mal_topp), (BREDDE, mal_bunn), 6)

    tekst = font.render(f"{poeng_v} - {poeng_h}", True, HVIT)
    skjerm.blit(tekst, (BREDDE//2 - tekst.get_width()//2, 10))

def main():
    pg.init()
    skjerm = pg.display.set_mode((BREDDE, HOYDE))
    pg.display.set_caption("Airhockey")
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

        venstre.flytt(taster, pg.K_w, pg.K_s, pg.K_a, pg.K_d)
        hoyre.flytt(taster, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)

        puck.oppdater()
        puck.kollisjon_med_kolle(venstre)
        puck.kollisjon_med_kolle(hoyre)

        mal = puck.vegger_og_mal()
        if mal == "mal_venstre":
            poeng_h += 1
            puck.reset(retning="venstre")
        elif mal == "mal_hoyre":
            poeng_v += 1
            puck.reset(retning="hoyre")

        tegn_bane(skjerm, poeng_v, poeng_h, font)
        venstre.tegn(skjerm)
        hoyre.tegn(skjerm)
        puck.tegn(skjerm)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()

