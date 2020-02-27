import pygame
from random import random, uniform, choice
from math import sin, cos, asin, pi, sqrt, acos
from os import environ
from time import time, sleep

# constants that can be changed
GROUND =(240, 255, 235)
PLANET =(230, 240, 215)
CENCOL =(255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 200,   0)
LIGHT = (200, 255, 200)
RED =   (255,   0,   0)
PINK =  (255, 200, 200)
HEAD =  (110, 110,   0)
TEXT =  ( 60,  60,  20)
RIMCOL =( 80, 140,  50)
FLAG = [(130, 200,  50)]

v = 120 # speed, pic/s?
v0 = v
r = 250 # sphere radius, pic
size = [600, 600] # size of screen
snake_len = 10
grow = 15 # growth by one food
dest = (0, -1)

# unchangable constants
score = 0
best = 0 # best score
center = [size[0] // 2, size[1] // 2]
pointsArray = []
foodArray = []
met = set()
pauseRec = pygame.Rect(50, 50, size[0] - 100, size[1] - 100)
buttonContinue = pygame.Rect(150, 200, size[0] - 300, 40)

environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (650 - center[0], 350 - center[1])
pygame.init()

screen = pygame.display.set_mode(size)

def anyfont(fontsize):
    return pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', fontsize)

# getting best score
try:
    f = open("cs/csrecords.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("cs/csrecords.txt", 'x')
f.close()

class Timer:

    def __init__(self, long):
        self.op = time()
        self.long = long
        self.rev = False

    def ison(self):
        if time() - self.op > self.long:
            return False
        return True

    def isonRev(self):
        if self.rev and not self.ison():
            return True
        return False

class Session(Timer):

    def __init__(self, p0, p1):
        self.op = time()
        self.p0 = p0
        self.p1 = p1

    def isOnFirst(self):
        if time() - self.op >= self.p0 + self.p1:
            self.op = time()
        if time() - self.op > self.p0:
            return False
        return True

    def finddir(piece):
        dir = ((center[0] - piece.x) / sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2), (center[1] - piece.y) / sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2))
        return (-dir[0], -dir[1])

timersDict = {"shapoval": Timer(0), "tarovik": Timer(0), "session": Session(20, 5)}

class Point:

    def __init__(self, x, y, vis):
        self.x = x
        self.y = y
        self.vis = vis
        self.speed = v0

    def draw(piece):
        if piece.vis:
            screen.blit(pygame.image.load('cs/' + piece.name.lower() + 'SmallVis.png'), (int(piece.x) - 17, int(piece.y) - 17))
        else:
            screen.blit(pygame.image.load('cs/' + piece.name.lower() + 'SmallNotVis.png'), (int(piece.x) - 17, int(piece.y) - 17))

class Trushin(Point):

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.met = False
        self.scr = 15
        self.name = "Trushin"

class Shapoval(Point):

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.met = False
        self.scr = 10
        self.name = "Shapoval"

    def finddir(piece):
        dir = ((center[0] - piece.x) / sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2), (center[1] - piece.y) / sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2))
        return (dir[0], dir[1])

class Tarovik(Point):

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.met = False
        self.scr = 17
        self.name = "Tarovik"

class Bragin(Point):

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.met = False
        self.scr = 20
        self.name = "Bragin"

class Podolsky(Point):

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.met = False
        self.scr = 14
        self.name = "Podolsky"

class InfWindow:

    def __init__(self, PointClass):

        if PointClass == "Shapoval":
            self.photo = pygame.image.load('cs/ShapovalBig.png')
            self.name = ["Шаповал Александр Борисович"]
            self.description = ["Преподает математический анализ.", '"Всегда приятно в аудитории сделать бяку"']
            self.ability = ["За опоздание ты оказался на елке позора.", "Мне за тебя очень стыдно.", "Все на карте в течение 8 секунд", "бегут от тебя."]
        elif PointClass == "Trushin":
            self.photo = pygame.image.load('cs/trushinBig.png')
            self.name = ["Трушин Дмитрий Витальевич"]
            self.description = ["Преподает линейную алгебру и геометрию.", '"Радостная новость - появилось идз!"']
            self.ability = ["Ты обратился к нему по имени-отчеству", "и несчастлив из-за идз.", "Трушин переворачивает твою матрицу."]
        elif PointClass == "Tarovik":
            self.photo = pygame.image.load('cs/tarovikBig.png')
            self.name = ["Таровик Елена Викторовна"]
            self.description = ["Преподает экономику.", '"В кр будут 3 темы: первая, вторая и третья"']
            self.ability = ["Пришло время твоих любимых", "самостоятельных!", "Если не успеешь за 4 секунд,", "тебе будет больно."]
        elif PointClass == "Bragin":
            self.photo = pygame.image.load('cs/braginBig.png')
            self.name = ["Брагин Сергей Дмитриевич"]
            self.description = ["Ведет семинары по информатике.", "Such a cinnamon roll!"]
            self.ability = ["Он не может навредить тебе!", "Пока ты под его защитой, никто", "не может тебе ничего сделать."]
        elif PointClass == "Podolsky":
            self.photo = pygame.image.load('cs/podolskyBig.png')
            self.name = ["Подольский", "Владимир Владимирович"]
            self.description = ["Преподает дискретную математику.", "Из свойств первое и третье очевидны,", "а во втором два случая:", "первый очевиден, второй теперь тоже"]
            self.ability = ["Ты получаешь дз, где первые задачи", "простые, а последние -", "как обухом по голове.", "От постоянной смены сложности", "тебе сложно двигаться ровно."]

    def drawInf(self):
        pygame.draw.rect(screen, (210, 240, 160), pauseRec)
        pygame.draw.rect(screen, HEAD, pauseRec, 3)
        screen.blit(self.photo, (center[0] - 82, 75))
        pos = 250
        for i in range(len(self.name)):
            screen.blit(anyfont(25).render(self.name[i], True, TEXT), (center[0] - len(self.name[i]) * 8.2, pos))
            pos += 25
        pos += 30
        for i in range(len(self.description)):
            screen.blit(anyfont(16).render(self.description[i], True, TEXT), (center[0] - len(self.description[i]) * 4.5, pos))
            pos += 18
        pos += 20
        for i in range(len(self.ability)):
            screen.blit(anyfont(19).render(self.ability[i], True, TEXT), (center[0] - len(self.ability[i]) * 5.8, pos))
            pos += 25
        pygame.display.flip()

def pause():
    global op
    pauseOp = time()
    pauseDone = False
    while not pauseDone:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if buttonContinue.collidepoint(mouse_pos):
                    pauseDone = True
                    op += time() - pauseOp
                    for timer in timersDict:
                        timersDict[timer].op += time() - pauseOp
            keystate = pygame.key.get_pressed()
            if keystate[13] != 0:
                pauseDone = True
                op += time() - pauseOp
                for timer in timersDict:
                    timersDict[timer].op += time() - pauseOp

def atg(dest):
    if (dest[0] + 10 ** (-6)) >= 0 and dest[1] > 0:
        return atan(dest[1] / (dest[0] + 10 ** (-6)))
    if (dest[0] + 10 ** (-6)) < 0 and dest[1] >= 0:
        return pi + atan(dest[1] / (dest[0] + 10 ** (-6)))
    if (dest[0] + 10 ** (-6)) <= 0 and dest[1] < 0:
        return pi + atan(dest[1] / (dest[0] + 10 ** (-6)))
    return 2 * pi + atan(dest[1] / (dest[0] + 10 ** (-6)))

def food():
    freeCor = findcor()
    possib = random()
    if possib < 0.2:
        foodArray.append(Shapoval(freeCor))
    elif possib < 0.4:
        foodArray.append(Trushin(freeCor))
    elif possib < 0.6:
        foodArray.append(Tarovik(freeCor))
    elif possib < 0.8:
        foodArray.append(Bragin(freeCor))
    elif possib < 1:
        foodArray.append(Podolsky(freeCor))

def findcor():
    while True:
        phi = uniform(0, 2 * pi)
        teta = uniform(-pi / 2, pi / 2)
        xfood = center[0] + r * cos(teta) * cos(phi)
        yfood = center[1] - r * sin(teta)
        if phi <= pi:
            if not collis((xfood, yfood), pointsArray, True, 5)[0]:
                return xfood, yfood, True
        else:
            if not collis((xfood, yfood), pointsArray, False, 5)[0]:
                return xfood, yfood, False

def gradient(cor=center, r=r, cenCol=CENCOL, rimCol=RIMCOL, delta=int(r / 2)):
    for i in range(delta):
        pygame.draw.circle(screen, (rimCol[0] + (cenCol[0] - rimCol[0]) / delta * i, rimCol[1] + (cenCol[1] - rimCol[1]) / delta * i, rimCol[2] + (cenCol[2] - rimCol[2]) / delta * i), cor, r - int(r / delta * i))

def drawmouse(point, color, r=10):
    if point.vis:
        pygame.draw.circle(screen, color, [int(point.x), int(point.y)], r)
        pygame.draw.circle(screen, BLACK, [int(point.x), int(point.y)], r, 1)
    else:
        pygame.draw.circle(screen, color, [int(point.x), int(point.y)], r, 1)

def drawpause():

    pygame.draw.rect(screen, (210, 230, 160), pauseRec)
    pygame.draw.rect(screen, HEAD, pauseRec, 3)
    pygame.draw.rect(screen, (160, 180, 110), buttonContinue)
    pygame.draw.rect(screen, HEAD, buttonContinue, 2)
    screen.blit(anyfont(30).render('Continue', True, TEXT), (225, 210))
    pygame.display.flip()

def drawfield():

    if timersDict["session"].isOnFirst():
        screen.fill(GROUND)
        gradient()
    else:
        screen.fill(RED)
        gradient(cenCol=RED, rimCol=BLACK)
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    sleep(0.02)

    for piece in foodArray:
        if piece.vis == False:
            Point.draw(piece)

    for i in range(0, len(pointsArray) - 1, 2):
        if not pointsArray[i].vis:
            drawmouse(pointsArray[i], FLAG[i % 1], 7)

    for i in range(0, len(pointsArray) - 1, 2):
        if pointsArray[i].vis:
            drawmouse(pointsArray[i], FLAG[i % 1], 7)

    for piece in foodArray:
        if piece.vis == True:
            Point.draw(piece)

    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)
    pygame.draw.circle(screen, BLACK, [center[0], center[1]], 10, 1)
    writescore()
    pygame.display.flip()

def writescore():
    global score
    screen.blit(anyfont(15).render('score: ' + str(int(score)), True, HEAD), (10, 10))
    screen.blit(anyfont(15).render('best score: ' + str(best), True, HEAD), (10, 25))

def collis(point, array, visi, delta=6):
    for el in array:
        if el.vis == visi:
            if point[0] < el.x + delta and point[0] > el.x - delta and point[1] < el.y + delta and point[1] > el.y - delta:
                return (True, el)
    return (False, None)

def newCor(point, dest=dest, speed=v0):
    step = speed * dt
    q = (center[0] + dest[0] * step, center[1] + dest[1] * step)
    if point.vis == True:
        ri = sqrt((point.x - center[0]) ** 2 + (point.y - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (point.x - center[0]) + (q[1] - center[1]) * (point.y - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = acos(tcos)
            r0 = sqrt(r ** 2 - ri ** 2 * sin(a) ** 2)
            alph = asin(max(-1, min(1, step / r)))
            if r0 == 0:
                return point
            tcos = ri * cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= pi - acos(tcos):
                if dest[0] + dest[1] == 1: ro = ri * cos(a) - r0 * cos(alph + acos(tcos))
                else: ro = ri * cos(a) - r0 * cos(acos(tcos) + alph)
                point.x -= dest[0] * abs(ro)
                point.y -= dest[1] * abs(ro)
            else:
                ro = ri * cos(a) + r0 * cos(pi - alph - acos(tcos))
                point.x -= dest[0] * ro
                point.y -= dest[1] * ro
                point.vis = False
        else:
            point.x -= step * dest[0]
            point.y -= step * dest[1]
        return point
    else:
        ri = sqrt((point.x - center[0]) ** 2 + (point.y - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (point.x - center[0]) + (q[1] - center[1]) * (point.y - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = acos(tcos)
            r0 = sqrt(r ** 2 - ri ** 2 * sin(a) ** 2)
            alph = asin(step / r)
            if r0 == 0:
                return point
            tcos = ri * cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= acos(tcos):
                if dest[0] + dest[1] == 1: ro = -ri * cos(a) + r0 * cos(-alph + acos(tcos))
                else: ro = ri * cos(a) - r0 * cos(-alph + acos(tcos))
                point.x += dest[0] * abs(ro)
                point.y += dest[1] * abs(ro)
            else:
                ro = ri * cos(a) - r0 * cos(acos(tcos) - alph)
                point.x -= dest[0] * ro
                point.y -= dest[1] * ro
                point.vis = True
        else:
            point.x += step * dest[0]
            point.y += step * dest[1]
        return point

def go():
    global score, done, snake_len, matrix, op, bragin, podolsky, v, v0
    # food effects
    if timersDict["tarovik"].isonRev():
        score -= 0.1
    if podolsky:
        mul = uniform(1, 3)
        if choice((True, False)):
            v = v0 * mul
        else:
            v = v0 / mul

    # changes snake coordinates
    for point in pointsArray:
        newCor(point, dest, v)

    # changes food coordinates
    for piece in foodArray:
        newCor(piece, dest, v)
        if Timer.ison(timersDict["shapoval"]) and not isinstance(piece, Bragin):
            newCor(piece, Shapoval.finddir(piece), v0 / 3)
        if not timersDict["session"].isOnFirst() and not isinstance(piece, Bragin):
            newCor(piece, Session.finddir(piece), v0 * 3)

    # collision checking
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 4)], True, 5)[0]:
        done = True
    foodcol = collis((center[0], center[1]), foodArray, True, 10)
    if foodcol[0]: # eating
        # removing expired effects
        matrix = 1
        timersDict["tarovik"].rev = False
        podolsky = False
        v = v0
        if foodcol[1].name not in met:
            InfWindow(foodcol[1].name).drawInf()
            pause()
            met.add(foodcol[1].name)
        if bragin:
            snake_len += grow
            bragin = False
        elif type(foodcol[1]) == Bragin:
            snake_len += grow
            bragin = True
            '''pauseOp = time()
            import spheresnakeRus
            drawfield()
            sleep(1)
            op += time() - pauseOp'''
        elif type(foodcol[1]) == Trushin:
            matrix = -1
            snake_len += grow
        elif type(foodcol[1]) == Shapoval:
            timersDict["shapoval"].op = time()
            timersDict["shapoval"].long = 8
            snake_len += grow
        elif type(foodcol[1]) == Tarovik:
            timersDict["tarovik"].op = time()
            timersDict["tarovik"].long = 4
            timersDict["tarovik"].rev = True
            snake_len += grow
        elif type(foodcol[1]) == Podolsky:
            snake_len += grow
            podolsky = True
        foodArray.remove(foodcol[1])
        score += foodcol[1].scr
        food()

    # checking if snake is growing, then deleting the first point
    if len(pointsArray) == snake_len: pointsArray.pop(0)
    pointsArray.append(Point(center[0], center[1], True))

    # drawing snake and food
    drawfield()

for i in range(5):
    food()

done = False
matrix = 1
bragin = False
podolsky = False
op = time()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keystate = pygame.key.get_pressed()
    if keystate[112] != 0:
        pauseOp = time()
        drawpause()
        pauseDone = False
        while not pauseDone:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if buttonContinue.collidepoint(mouse_pos):
                        pauseDone = True
        op += time() - pauseOp
        for timer in timersDict:
            timersDict[timer].op += time() - pauseOp

    elif keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
        if dest != (-1 / sqrt(2) * matrix, 1 / sqrt(2) * matrix):
            dest = (1 / sqrt(2) * matrix, -1 / sqrt(2) * matrix)
    elif keystate[pygame.K_UP] and keystate[pygame.K_LEFT]:
        if dest != (1 / sqrt(2) * matrix, 1 / sqrt(2) * matrix):
            dest = (-1 / sqrt(2) * matrix, -1 / sqrt(2) * matrix)
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
        if dest != (-1 / sqrt(2) * matrix, -1 / sqrt(2) * matrix):
            dest = (1 / sqrt(2) * matrix, 1 / sqrt(2) * matrix)
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
        if dest != (1 / sqrt(2) * matrix, -1 / sqrt(2) * matrix):
            dest = (-1 / sqrt(2) * matrix, 1 / sqrt(2) * matrix)
    elif keystate[pygame.K_UP]:
        if dest != (0, 1 * matrix):
            dest = (0, -1 * matrix)
    elif keystate[pygame.K_DOWN]:
        if dest != (0, -1 * matrix):
            dest = (0, 1 * matrix)
    elif keystate[pygame.K_RIGHT]:
        if dest != (-1 * matrix, 0):
            dest = (1 * matrix, 0)
    elif keystate[pygame.K_LEFT]:
        if dest != (1 * matrix, 0):
            dest = (-1 * matrix, 0)

    ed = time()
    dt = ed - op
    op = ed
    if dt != 0:
        go()

if score > best:
    best = int(score)
    screen.fill(LIGHT)
    screen.blit(anyfont(50).render('NEW HIGH SCORE', True, GREEN), (65, 200))
else:
    screen.fill(PINK)
    screen.blit(anyfont(50).render('YOU HAVE LOST', True, RED), (85, 200))

writescore()
pygame.display.flip()
f = open("cs/csrecords.txt", 'w')
f.write(str(best))
f.close()
sleep(2)

# pygame.quit()
