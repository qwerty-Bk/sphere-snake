import random, pygame, math
from time import time, sleep
from os import environ

# constants that can be changed
GROUND =(250, 255, 235)
PLANET =(230, 240, 215)
CENCOL =(255, 255, 255)
RIMCOL =(130, 160, 100)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 200,   0)
LIGHT = (200, 255, 200)
RED =   (255,   0,   0)
PINK =  (255, 200, 200)
HEAD =  (  0,   0, 200)
ELEPH = (200, 200, 200)
SERIAS= RED
FLAG = [(255, 180, 0), WHITE, GREEN]

v = 120 # speed, pic/s?
v0 = v
r = 250 # sphere radius, pic
size = [600, 600] # size of screen
snake_len = 10
grow = 15 # growth by one food
dest = (0, -1)

# unchangeable constants
score = 0
best = 0 # best score
center = [size[0] // 2, size[1] // 2]
pointsArray = []
foodArray = []
pauseRec = pygame.Rect(50, 50, size[0] - 100, size[1] - 100)
buttonContinue = pygame.Rect(150, 200, size[0] - 300, 40)
buttonInformation = pygame.Rect(150, 270, size[0] - 300, 40)
buttonEleph = pygame.Rect(150, 270, size[0] - 300, 40)
buttonTamer = pygame.Rect(150, 340, size[0] - 300, 40)
buttonSerias = pygame.Rect(150, 410, size[0] - 300, 40)
menuButtons = (
    (buttonContinue, 'Continue'),
    (buttonInformation, 'Information')
)
foodButtons = (
    (buttonContinue, 'Continue'),
    (buttonEleph, 'Bishop'),
    (buttonTamer, 'Snake Charmer'),
    (buttonSerias, 'Serias')
)

environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (650 - center[0], 350 - center[1])
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('india/IndiaSong.ogg')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.pause()
elephImg = pygame.image.load('india/myelephant.png')
notElephImg = pygame.image.load('india/mynotelephant.png')
bigElephImg = pygame.image.load('india/bigelephant.png')
tamerImg = pygame.image.load('india/tamer.png')
notTamerImg = pygame.image.load('india/nottamer.png')
bigTamerImg = pygame.image.load('india/bigtamer.png')
seriasImg = pygame.image.load('india/serias.png')
notSeriasImg = pygame.image.load('india/notserias.png')
bigSeriasImg = pygame.image.load('india/bigserias.png')
screen = pygame.display.set_mode(size)

def anyfont(fontsize):
    return pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', fontsize)

# getting best score
try:
    f = open("india/indrecords.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("india/indrecords.txt", 'x')
f.close()

class Timer:

    def __init__(self, long):
        self.op = time()
        self.long = long

    def ison(self):
        if time() - self.op > self.long:
            return False
        else:
            return True

danceTimer = Timer(0)

class Point:

    def __init__(self, x, y, vis):
        self.x = x
        self.y = y
        self.vis = vis
        self.speed = v0

    def draw(self):
        if self.vis:
            screen.blit(self.img, (int(self.x) - self.img.get_width() // 2, int(self.y) - self.img.get_height() // 2))
        else:
            screen.blit(self.imgNot, (int(self.x) - self.imgNot.get_width() // 2, int(self.y) - self.imgNot.get_height() // 2))

    def drawInf(piece):
        pygame.draw.rect(screen, (210, 230, 160), pauseRec)
        pygame.draw.rect(screen, BLACK, pauseRec, 3)
        screen.blit(piece.imgBig, (size[0] // 2 - piece.imgBig.get_width() // 2, size[1] // 2 - piece.imgBig.get_height() // 2))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            keystate = pygame.key.get_pressed()
            if sum(keystate) != 0:
                done = True

class Elephant(Point):

    img = elephImg
    imgNot = notElephImg
    imgBig = bigElephImg
    info = ""

    def __init__(self, place=(0, 0, True)):
        self.x, self.y, self.vis = place
        self.scr = 20

class Serias(Point):

    img = seriasImg
    imgNot = notSeriasImg
    imgBig = bigSeriasImg

    def __init__(self, place=(0, 0, True)):
        self.x, self.y, self.vis = place
        self.color = SERIAS
        self.scr = random.uniform(-15, 25)

class Tamer(Point):

    imgBig = bigTamerImg
    img = tamerImg
    imgNot = notTamerImg

    def __init__(self, place=(0, 0, True)):
        self.x, self.y, self.vis = place
        self.color = GREEN
        self.scr = 17

    def dir(dest):
        for piece in foodArray:
            if type(piece) == Tamer:
                destTamer = ((piece.x - center[0]) / ((piece.x - center[0]) ** 2 + (piece.y - center[1]) ** 2) ** 0.5, (piece.y - center[1]) / ((piece.x - center[0]) ** 2 + (piece.y - center[1]) ** 2) ** 0.5)
                if atg(destTamer) - atg(dest) < math.pi:
                    newAngle = atg(destTamer) / 50 + 49 * atg(dest) / 50
                    return (math.cos(newAngle), math.sin(newAngle))
                else:
                    newAngle = (2 * math.pi - atg(destTamer)) / 50 + 49 * atg(dest) / 50
                    return (math.cos(newAngle), math.sin(newAngle))
        return dest

def atg(dest):
    if (dest[0] + 10 ** (-6)) >= 0 and dest[1] > 0:
        return math.atan(dest[1] / (dest[0] + 10 ** (-6)))
    if (dest[0] + 10 ** (-6)) < 0 and dest[1] >= 0:
        return math.pi + math.atan(dest[1] / (dest[0] + 10 ** (-6)))
    if (dest[0] + 10 ** (-6)) <= 0 and dest[1] < 0:
        return math.pi + math.atan(dest[1] / (dest[0] + 10 ** (-6)))
    return 2 * math.pi + math.atan(dest[1] / (dest[0] + 10 ** (-6)))

def food():
    freeCor = findcor()
    possib = random.random()
    if possib < 0.3:
        foodArray.append(Serias(freeCor))
    elif possib < 0.6:
        foodArray.append(Elephant(freeCor))
    else:
        foodArray.append(Tamer(freeCor))

def findcor():
    while True:
        phi = random.uniform(0, 2 * math.pi)
        teta = random.uniform(-math.pi / 2, math.pi / 2)
        xfood = center[0] + r * math.cos(teta) * math.cos(phi)
        yfood = center[1] - r * math.sin(teta)
        if phi <= math.pi:
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
    pygame.draw.rect(screen, BLACK, pauseRec, 3)
    for b in menuButtons:
        pygame.draw.rect(screen, (160, 180, 110), b[0])
        pygame.draw.rect(screen, BLACK, b[0], 2)
        screen.blit(anyfont(30).render(b[1], True, BLACK), (b[0].x + b[0].size[0] // 2 - 9 * len(b[1]), b[0].y + b[0].size[1] / 4))
    pygame.display.flip()

def pause():
    drawpause()
    pauseDone = False
    while not pauseDone:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if buttonContinue.collidepoint(mouse_pos):
                    pauseDone = True
                if buttonInformation.collidepoint(mouse_pos):
                    inf()
                    drawpause()
                    break
        keystate = pygame.key.get_pressed()
        if keystate[13] != 0:
            pauseDone = True
    return True

def inf():
    pygame.draw.rect(screen, (210, 230, 160), pauseRec)
    pygame.draw.rect(screen, BLACK, pauseRec, 3)
    for b in foodButtons:
        pygame.draw.rect(screen, (160, 180, 110), b[0])
        pygame.draw.rect(screen, BLACK, b[0], 2)
        screen.blit(anyfont(30).render(b[1], True, BLACK), (b[0].x + b[0].size[0] // 2 - 9 * len(b[1]), b[0].y + b[0].size[1] / 4))
    pygame.display.flip()
    pauseDone = False
    while not pauseDone:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if buttonContinue.collidepoint(mouse_pos):
                    pauseDone = True
                elif buttonEleph.collidepoint(mouse_pos):
                    Point.drawInf(Elephant())
                    pauseDone = True
                elif buttonTamer.collidepoint(mouse_pos):
                    Point.drawInf(Tamer())
                    pauseDone = True
                elif buttonSerias.collidepoint(mouse_pos):
                    Point.drawInf(Serias())
                    pauseDone = True

def drawfield():

    screen.fill(GROUND)
    gradient()
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    sleep(0.02)

    for piece in foodArray:
        if piece.vis == False:
            piece.draw()

    for i in range(0, len(pointsArray) - 1, 2):
        if not pointsArray[i].vis:
            drawmouse(pointsArray[i], FLAG[i % 3], 7)

    for i in range(0, len(pointsArray) - 1, 2):
        if pointsArray[i].vis:
            drawmouse(pointsArray[i], FLAG[i % 3], 7)

    for piece in foodArray:
        if piece.vis == True:
            piece.draw()

    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)
    writescore()
    pygame.display.flip()

def writescore():
    global score
    screen.blit(anyfont(15).render('score: ' + str(int(score)), True, HEAD), (10, 10))
    screen.blit(anyfont(15).render('best score: ' + str(best), True, HEAD), (10, 25))

def collis(point, array, visi, delta=4):
    for el in array:
        if el.vis == visi:
            if point[0] < el.x + delta and point[0] > el.x - delta and point[1] < el.y + delta and point[1] > el.y - delta:
                return (True, el)
    return (False, None)

def newCor(point, dest=dest, speed=v0):
    step = speed * dt
    q = (center[0] + dest[0] * step, center[1] + dest[1] * step)
    if point.vis == True:
        ri = math.sqrt((point.x - center[0]) ** 2 + (point.y - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (point.x - center[0]) + (q[1] - center[1]) * (point.y - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = math.acos(tcos)
            r0 = math.sqrt(r ** 2 - ri ** 2 * math.sin(a) ** 2)
            alph = math.asin(step / r)
            if r0 == 0:
                return point
            tcos = ri * math.cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= math.pi - math.acos(tcos):
                if dest[0] + dest[1] == 1: ro = ri * math.cos(a) - r0 * math.cos(alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) + alph)
                point.x -= dest[0] * abs(ro)
                point.y -= dest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) + r0 * math.cos(math.pi - alph - math.acos(tcos))
                point.x -= dest[0] * ro
                point.y -= dest[1] * ro
                point.vis = False
        else:
            point.x -= step * dest[0]
            point.y -= step * dest[1]
        return point
    else:
        ri = math.sqrt((point.x - center[0]) ** 2 + (point.y - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (point.x - center[0]) + (q[1] - center[1]) * (point.y - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = math.acos(tcos)
            r0 = math.sqrt(r ** 2 - ri ** 2 * math.sin(a) ** 2)
            alph = math.asin(step / r)
            if r0 == 0:
                return point
            tcos = ri * math.cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= math.acos(tcos):
                if dest[0] + dest[1] == 1: ro = -ri * math.cos(a) + r0 * math.cos(-alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(-alph + math.acos(tcos))
                point.x += dest[0] * abs(ro)
                point.y += dest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) - alph)
                point.x -= dest[0] * ro
                point.y -= dest[1] * ro
                point.vis = True
        else:
            point.x += step * dest[0]
            point.y += step * dest[1]
        return point

def inDiap(old, new): # it is bad if the function returns True
    angel = abs(atg((-old[0], old[1])) - atg((new[0], -new[1])))
    if min(angel, abs(math.pi - angel)) > math.pi / 4 - 0.1:
        return False
    return True

def go():
    global score, done, snake_len, bishop, danceTimer, snakeTamer
    # changes snake coordinates
    for point in pointsArray:
        #print('newcor for', point.x, point.y)
        newCor(point, dest)

    # changes food coordinates
    for piece in foodArray:
        newCor(piece, dest)
        if Timer.ison(danceTimer):
            danceDir = random.uniform(0, 2 * math.pi)
            newCor(piece, (math.cos(danceDir), math.sin(danceDir)), v0 / 1.5)
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    # collision checking
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 4)], True, 5)[0]:
        done = True
    foodcol = collis((center[0], center[1]), foodArray, True, 10)
    if foodcol[0]: # eating
        bishop = False
        if type(foodcol[1]) == Elephant:
            bishop = True
            snake_len += grow
        elif type(foodcol[1]) == Serias:
            danceTimer = Timer(10)
            pygame.mixer.music.unpause()
        elif type(foodcol[1]) == Tamer:
            snake_len += grow
        else:
            snake_len += grow
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
bishop = False
q = (center[0], center[1])
op = time()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keystate = pygame.key.get_pressed()
    if keystate[112] != 0:
        pauseOp = time()
        pause()
        op += time() - pauseOp
        danceTimer.op += time() - pauseOp
    elif keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
        if not inDiap(dest, (1 / math.sqrt(2), -1 / math.sqrt(2))):
            dest = (1 / math.sqrt(2), -1 / math.sqrt(2))
    elif keystate[pygame.K_UP] and keystate[pygame.K_LEFT]:
        if not inDiap(dest, (-1 / math.sqrt(2), -1 / math.sqrt(2))):
            dest = (-1 / math.sqrt(2), -1 / math.sqrt(2))
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
        if not inDiap(dest, (1 / math.sqrt(2), 1 / math.sqrt(2))):
            dest = (1 / math.sqrt(2), 1 / math.sqrt(2))
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
        if not inDiap(dest, (-1 / math.sqrt(2), 1 / math.sqrt(2))):
            dest = (-1 / math.sqrt(2), 1 / math.sqrt(2))
    elif keystate[pygame.K_UP] and not bishop:
        if not inDiap(dest, (0, -1)):
            dest = (0, -1)
    elif keystate[pygame.K_DOWN] and not bishop:
        if not inDiap(dest, (0, 1)):
            dest = (0, 1)
    elif keystate[pygame.K_RIGHT] and not bishop:
        if not inDiap(dest, (1, 0)):
            dest = (1, 0)
    elif keystate[pygame.K_LEFT] and not bishop:
        if not inDiap(dest, (-1, 0)):
            dest = (-1, 0)

    dest = Tamer.dir(dest)

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
f = open("india/indrecords.txt", 'w')
f.write(str(best))
f.close()
sleep(2)

# pygame.quit()
