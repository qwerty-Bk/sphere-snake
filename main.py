import pygame
from os import environ
import sys

BACKGROUND = (230, 255, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTONBACK = (200, 235, 150)
BUTTONBORDER = (80, 115, 30)
TEXT = (30, 60, 0)

size = [600, 600] # size of screen
center = [size[0] // 2, size[1] // 2]


environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (650 - center[0], 350 - center[1])
pygame.init()
def anyfont(fontsize):
    return pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', fontsize)

class button():

    def __init__(self, _x0, _y0, _h, _backColor=BUTTONBACK, _borderColor=BUTTONBORDER, _text="", _mod=""):
        self.x0 = _x0;
        self.y0 = _y0;
        self.width = size[0] - 2 * _x0;
        self.height = _h;
        self.backColor = _backColor;
        self.borderColor = _borderColor;
        self.rect = pygame.Rect(_x0, _y0, self.width, _h);
        self.text = _text
        self.on = False
        self.mod = _mod

    def backColorOn(self):
        return (max(0, self.backColor[0] - 50 * self.on), max(0, self.backColor[1] - 50 * self.on), max(0, self.backColor[2] - 50 * self.on))

    def draw(self):
        pygame.draw.rect(screen, self.backColorOn(), self.rect)
        pygame.draw.rect(screen, self.borderColor, self.rect, 3)
        screen.blit(anyfont(22).render(self.text, True, BACKGROUND), (center[0] - 6.8*len(self.text), self.y0 + 8))
        screen.blit(anyfont(22).render(self.text, True, TEXT), (center[0] - 7*len(self.text), self.y0 + 7))

def stopRunning():
    running = False

buttonInf = button(70, 130, 30, _text="Exit", _mod="")
buttonClassic = button(70, 180, 30, _text="Classical sphere", _mod="plain.spheresnakegame")
buttonRussia = button(70, 230, 30, _text="Russian everyday life", _mod="russia.spheresnakeRus")
buttonIndia = button(70, 280, 30, _text="Indian festival", _mod="india.spheresnakeInd")
buttonGermany = button(70, 330, 30, _text="Germany's anabasis", _mod="germany.spheresnakeGerm")
buttonFrance = button(70, 380, 30, _text="French evening", _mod="france.spheresnakeFran")
buttonHyper = button(70, 430, 30, _text="Hyperbolic space", _mod="hyperbolic.hyperbolicsnake")
buttonCs = button(70, 480, 30, _text="CS AMI", _mod="cs.spheresnakeCs1")

buttonsMain = [buttonInf, buttonClassic, buttonRussia, buttonIndia, buttonGermany, buttonFrance, buttonHyper, buttonCs]

def buttonUpdate(buttonsNow=buttonsMain):
    for b in buttons:
        b.draw()
    pygame.display.update()

def fullUpdate(buttonsNow=buttonsMain):
    screen.fill(BACKGROUND)
    screen.blit(anyfont(30).render('Welcome to Sphere Snake', True, WHITE), (center[0] - 212, 52))
    screen.blit(anyfont(30).render('Welcome to Sphere Snake', True, TEXT), (center[0] - 210, 50))
    buttonUpdate(buttonsNow)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
# pygame.display.set_icon(None)

buttons = buttonsMain
fullUpdate()

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for b in buttons:
        if b.rect.collidepoint(mouse_pos):
            b.on = True
        else:
            b.on = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonInf.rect.collidepoint(mouse_pos):
                running = False
            for b in buttons[1:]:
                if b.rect.collidepoint(mouse_pos):
                    x = __import__(b.mod)
                    del x
                    sys.modules.pop(b.mod)
                    fullUpdate()
    buttonUpdate()
    # pygame.display.flip()


pygame.quit()
