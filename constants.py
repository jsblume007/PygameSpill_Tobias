import math

BREDDE, HOYDE = 900, 500
FPS = 60

RADIUS_KOLLE = 25
RADIUS_PUCK = 14

FART_KOLLE = 6
FRIKSJON = 0.995
MAKS_FART_PUCK = 12

MAL_APNING = 160

HVIT = (240, 240, 240)
GRA = (130, 130, 130)
BLA = (80, 160, 255)
ROD = (255, 90, 90)
BAKGRUNN = (20, 24, 28)
GRONN = (100, 255, 160)

def klem(x, lav, hoy):
    return max(lav, min(hoy, x))

def avstand(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

