import random, pygame, math, time
from os import environ

# constants that can be changed
GROUND =(250, 255, 235)
PLANET =(230, 240, 215)
CENCOL =(255, 255, 255)
RIMCOL =(130, 160, 100) # 35
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 200,   0)
LIGHT = (200, 255, 200)
RED =   (255,   0,   0)
PINK =  (255, 200, 200)
BLUE =  (  0,   0, 255)
HEAD =  ( 95, 130,  15)
foodtypes = ("woman", "man", 'vine', "usual")
def vineoutline(x, y):
    return ((int(x - 9), int(y - 9)), (int(x - 1), int(y)), (int(x - 1), int(y + 6)), (int(x - 3), int(y + 8)), (int(x + 3), int(y + 8)), (int(x + 1), int(y + 6)), (int(x + 1), int(y)), (int(x + 9), int(y - 9)), (int(x + 7), int(y - 7)), (int(x - 7), int(y - 7)))
FLAG = (RED, BLUE, WHITE)

v = 120 # speed, pic/s?
v0 = v
r = 250 # sphere radius, pic
size = [600, 600] # size of screen
snake_len = 10
grow = 15 # growth by one food

# unchangable constants
score = 0
best = 0 # best score
center = [size[0] // 2, size[1] // 2]
pointsArray = []
foodArray = []

environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (650 - center[0], 350 - center[1])
pygame.init()

screen = pygame.display.set_mode(size)
fontlose = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 50)
fontscore = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 15)

# getting best score
try:
    f = open("france/franrecords.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("france/franrecords.txt", 'x')
f.close()

class Timer:

    def __init__(self, long):
        self.op = time.time()
        self.long = long

    def ison(self):
        if time.time() - self.op > self.long:
            return False
        return True

drunkTimer = Timer(0)

class Point:

    def __init__(self, x, y, vis):
        self.x = x
        self.y = y
        self.vis = vis

class Food(Point):

    def __init__(self, type='usual'):

        self.x, self.y, self.vis, self.type = Food.findcor()
        if type != 'usual':
            self.type = type
            self.scr = -40
            self.speed = v * 1.5
            self.dir = Food.finddir((self.x, self.y), self.vis)
            self.timer = Timer(5)
        elif self.type == 'usual':
            self.scr = random.uniform(1, 10)
            self.color = (random.randint(0, 105), random.randint(0, 105), random.randint(0, 105))
        elif self.type == 'woman':
            self.scr = 20
            self.color = RED
        elif self.type == 'vine':
            self.scr = 15
            self.color = (150, 0, 50)

    def findcor():
        while True:
            phi = random.uniform(0, 2 * math.pi)
            teta = random.uniform(-math.pi / 2, math.pi / 2)
            xfood = center[0] + r * math.cos(teta) * math.cos(phi)
            yfood = center[1] - r * math.sin(teta)
            if phi <= math.pi:
                if not collis((xfood, yfood), pointsArray, True, 5)[0]:
                    possib = random.random()
                    if possib < 0.3: typefood = "woman"
                    elif possib < 0.5: typefood = 'vine'
                    else: typefood = "usual"
                    return xfood, yfood, True, typefood
            else:
                if not collis((xfood, yfood), pointsArray, False, 5)[0]:
                    possib = random.random()
                    if possib < 0.3: typefood = "woman"
                    elif possib < 0.5: typefood = 'vine'
                    else: typefood = "usual"
                    return xfood, yfood, False, typefood

    def finddir(cor, vis):
        dir = (-(center[0] - cor[0]) / math.sqrt((center[0] - cor[0]) ** 2 + (center[1] - cor[1]) ** 2), -(center[1] - cor[1]) / math.sqrt((center[0] - cor[0]) ** 2 + (center[1] - cor[1]) ** 2))
        return dir

def gradient(cor=center, r=r, cenCol=CENCOL, rimCol=RIMCOL, delta=int(r / 2)):
    for i in range(delta):
        pygame.draw.circle(screen, (rimCol[0] + (cenCol[0] - rimCol[0]) / delta * i, rimCol[1] + (cenCol[1] - rimCol[1]) / delta * i, rimCol[2] + (cenCol[2] - rimCol[2]) / delta * i), cor, r - int(r / delta * i))

def womandir(piece):
    return ((piece.x - center[0]) / math.sqrt((piece.x - center[0]) ** 2 + (piece.y - center[1]) ** 2), (piece.y - center[1]) / math.sqrt((piece.x - center[0]) ** 2 + (piece.y - center[1]) ** 2))

def drawwoman(point, vis, color=RED, r=5):
    if vis:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1]) - r], r)
        pygame.draw.circle(screen, BLACK, [int(point[0]), int(point[1]) - r], r, 1)
        pygame.draw.polygon(screen, color, [(int(point[0]), int(point[1])), (int(point[0] - r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2)), (int(point[0] + r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2))])
        pygame.draw.lines(screen, BLACK, True, [(int(point[0]), int(point[1])), (int(point[0] - r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2)), (int(point[0] + r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2))])
    else:
        pygame.draw.lines(screen, color, True, [(int(point[0]), int(point[1])), (int(point[0] - r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2)), (int(point[0] + r * math.sqrt(3) / 2), int(point[1] + r * 3 / 2))])
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1]) - r], r, 1)

def drawman(point, vis, color=BLUE, r=5):
    if vis:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1]) - r], r)
        pygame.draw.circle(screen, BLACK, [int(point[0]), int(point[1]) - r], r, 1)
        pygame.draw.polygon(screen, color, [(int(point[0]), int(point[1]) + 2 * r), (int(point[0] - r * math.sqrt(3) / 2), int(point[1])), (int(point[0] + r * math.sqrt(3) / 2), int(point[1]))])
        pygame.draw.lines(screen, BLACK, True, [(int(point[0]), int(point[1])), (int(point[0] - r * math.sqrt(3) / 2), int(point[1])), (int(point[0] + r * math.sqrt(3) / 2), int(point[1]))])
    else:
        pygame.draw.lines(screen, color, True, [(int(point[0]), int(point[1])), (int(point[0] - r * math.sqrt(3) / 2), int(point[1])), (int(point[0] + r * math.sqrt(3) / 2), int(point[1]))])
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1]) - r], r, 1)

def drawvine(piece):
    if piece.vis:
        pygame.draw.polygon(screen, piece.color, vineoutline(piece.x, piece.y))
        pygame.draw.lines(screen, BLACK, True, vineoutline(piece.x, piece.y))
    else:
        pygame.draw.lines(screen, BLACK, True, vineoutline(piece.x, piece.y))

def drawmouse(point, color, vis, r=10):
    if vis:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r)
        pygame.draw.circle(screen, BLACK, [int(point[0]), int(point[1])], r, 1)
    else:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r, 1)

def drawfield():
    if Timer.ison(drunkTimer):
        screen.fill((255, 220, 220))
        screen.blit(fontscore.render('Vine: ' + str(int((-time.time() + drunkTimer.op + drunkTimer.long) * 100) / 100), True, RED), (center[0] - 50, 10))
    else:
        screen.fill(GROUND)
    gradient()
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)

    for piece in foodArray:
        if piece.vis == False:
            if piece.type == "woman":
                drawwoman((piece.x, piece.y), piece.vis)
            elif piece.type == "man": drawman((piece.x, piece.y), piece.vis)
            elif piece.type == 'vine': drawvine(piece)
            elif piece.type == "usual": drawmouse((piece.x, piece.y), piece.color, piece.vis)

    for i in range(0, len(pointsArray) - 1, 2):
        if not pointsArray[i].vis:
            drawmouse((pointsArray[i].x, pointsArray[i].y), FLAG[i % 3], pointsArray[i].vis, 7)

    for i in range(0, len(pointsArray) - 1, 2):
        if pointsArray[i].vis:
            drawmouse((pointsArray[i].x, pointsArray[i].y), FLAG[i % 3], pointsArray[i].vis, 7)

    for piece in foodArray:
        if piece.vis == True:
            if piece.type == "woman": drawwoman((piece.x, piece.y), piece.vis)
            elif piece.type == "man": drawman((piece.x, piece.y), piece.vis)
            elif piece.type == 'vine': drawvine(piece)
            elif piece.type == "usual": drawmouse((piece.x, piece.y), piece.color, piece.vis)


    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)
    writescore()
    pygame.display.flip()

def writescore():
    global score
    screen.blit(fontscore.render('score: ' + str(int(score)), True, HEAD), (10, 10))
    screen.blit(fontscore.render('best score: ' + str(best), True, HEAD), (10, 25))

def collis(point, array, visi, delta=4):
    for el in array:
        if el.vis == visi:
            if point[0] < el.x + delta and point[0] > el.x - delta and point[1] < el.y + delta and point[1] > el.y - delta:
                return (True, el)
    return (False, None)

def newCor(point, ourdest=None):
    if ourdest == None:
        ourdest = dest
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
                if ourdest[0] + ourdest[1] == 1: ro = ri * math.cos(a) - r0 * math.cos(alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) + alph)
                point.x -= ourdest[0] * abs(ro)
                point.y -= ourdest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) + r0 * math.cos(math.pi - alph - math.acos(tcos))
                point.x -= ourdest[0] * ro
                point.y -= ourdest[1] * ro
                point.vis = False
        else:
            point.x -= step * ourdest[0]
            point.y -= step * ourdest[1]
        return point
    else:
        ri = math.sqrt((point.x - center[0]) ** 2 + (point.y - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (point.x - center[0]) + (q[1] - center[1]) * (point.y - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = math.acos(tcos)
            r0 = math.sqrt(max(r ** 2 - ri ** 2 * math.sin(a) ** 2, 0))
            alph = math.asin(step / r)
            if r0 == 0:
                return point
            tcos = ri * math.cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= math.acos(tcos):
                if ourdest[0] + ourdest[1] == 1: ro = -ri * math.cos(a) + r0 * math.cos(-alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(-alph + math.acos(tcos))
                point.x += ourdest[0] * abs(ro)
                point.y += ourdest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) - alph)
                point.x -= ourdest[0] * ro
                point.y -= ourdest[1] * ro
                point.vis = True
        else:
            point.x += step * ourdest[0]
            point.y += step * ourdest[1]
        return point

def go():
    global score, pointsArray, foodArray, q, dest, snake_len, done, v, drunkTimer
    # changes snake coordinates
    for point in pointsArray:
        newCor(point)

    # changes food coordinates
    for piece in foodArray:
        newCor(piece)
        if piece.type == 'man':
            if not Timer.ison(piece.timer):
                foodArray.remove(piece)
            piece.dir = Food.finddir((piece.x, piece.y), piece.vis)
            newCor(piece, piece.dir)

    # collision checking
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 7)], True, 3)[0]:
        done = True
    foodcol = collis((center[0], center[1]), foodArray, True, 10)
    if foodcol[0]: # eating
        v = v0
        foodArray.remove(foodcol[1])
        if foodcol[1].type == 'vine':
            drunkTimer.op = time.time()
            drunkTimer.long = 10
        if foodcol[1].type == 'woman':
            foodArray.append(Food('man'))
            foodArray.append(Food())
        elif foodcol[1].type != "man":
            foodArray.append(Food())
            snake_len += grow
        score += foodcol[1].scr

    # checking if snake is growing, then deleting the first point
    if len(pointsArray) == snake_len: pointsArray.pop(0)

    # drawing snake and food
    time.sleep(0.02)
    pointsArray.append(Point(center[0], center[1], True))
    drawfield()

for i in range(5): foodArray.append(Food())
drawfield()
pygame.display.flip()

done = False
dest = (0, -1)
q = (center[0], center[1])
op = time.time()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if Timer.ison(drunkTimer):
        for piece in foodArray:
            if piece.type == 'woman':
                dest = womandir(piece)
                break
    keystate = pygame.key.get_pressed()
    if keystate[13] != 0:
        pointsArray = [Point(center[0], center[1], True)]
        snake_len = 10
        score = 0
        drawfield()
    elif keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
        if dest != (-1 / math.sqrt(2), 1 / math.sqrt(2)):
            dest = (1 / math.sqrt(2), -1 / math.sqrt(2))
    elif keystate[pygame.K_UP] and keystate[pygame.K_LEFT]:
        if dest != (1 / math.sqrt(2), 1 / math.sqrt(2)):
            dest = (-1 / math.sqrt(2), -1 / math.sqrt(2))
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
        if dest != (-1 / math.sqrt(2), -1 / math.sqrt(2)):
            dest = (1 / math.sqrt(2), 1 / math.sqrt(2))
    elif keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
        if dest != (1 / math.sqrt(2), -1 / math.sqrt(2)):
            dest = (-1 / math.sqrt(2), 1 / math.sqrt(2))
    elif keystate[pygame.K_UP]:
        if dest != (0, 1):
            dest = (0, -1)
    elif keystate[pygame.K_DOWN]:
        if dest != (0, -1):
            dest = (0, 1)
    elif keystate[pygame.K_RIGHT]:
        if dest != (-1, 0):
            dest = (1, 0)
    elif keystate[pygame.K_LEFT]:
        if dest != (1, 0):
            dest = (-1, 0)

    ed = time.time()
    step = v * (ed - op)
    op = ed
    if step != 0:
        q = (center[0] + dest[0] * step, center[1] + dest[1] * step)
        go()

if score > best:
    best = int(score)
    screen.fill(LIGHT)
    screen.blit(fontlose.render('NEW HIGH SCORE', True, GREEN), (65, 200))
else:
    screen.fill(PINK)
    screen.blit(fontlose.render('YOU HAVE LOST', True, RED), (85, 200))
writescore()
pygame.display.flip()
f = open("france/franrecords.txt", 'w')
f.write(str(best))
f.close()
time.sleep(2)

# pygame.quit()
