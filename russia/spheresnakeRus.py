import random, pygame, math, time
from os import environ

# constants that can be changed
GROUND =(250, 255, 235)
PLANET =(230, 240, 215)
#CENCOL =(250, 255, 230)
CENCOL =(255, 255, 255)
RIMCOL =(130, 160, 100) # 35
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 200,   0)
LIGHT = (200, 255, 200)
RED =   (255,   0,   0)
PINK =  (255, 200, 200)
HEAD =  RED
FLAG = [RED, (0, 0, 255), WHITE]
vodkaTimer = None
medvedTimer = None

v = 120 # speed, pic/s?
v0 = v
r = 250 # sphere radius, pic
size = [600, 600] # size of screen
snake_len = 10
grow = 15 # growth by one food
dest = (0, -1)
step = 10

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
    f = open("russia/records.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("russia/records.txt", 'x')
f.close()

class Timer:

    def __init__(self, long):
        self.op = time.time()
        self.long = long

    def ison(self):
        if time.time() - self.op > self.long:
            return False
        else:
            return True

class Point:

    def __init__(self, x, y, vis):
        self.x = x
        self.y = y
        self.vis = vis

def newCor(point, dest, step):
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

class Food:

    def __init__(self, x=center[0], y=center[0], vis=True, type='usual', color=BLACK, scr=0):
        if scr != 0:
            self.x, self.y, self.vis, self.type, self.color, self.scr = x, y, vis, type, color, scr
        else:
            self.x, self.y, self.vis, self.type = Food.findcor()
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if self.type == 'usual':
                self.scr = random.uniform(1, 10)
            elif self.type == 'medved': self.scr = 20
            elif self.type == 'vodka': self.scr = 15

    def copy(self):

        return Food(self.x, self.y, self.vis, self.type, self.color, self.scr)

    def findcor():

        while True:
            phi = random.uniform(0, 2 * math.pi)
            teta = random.uniform(-math.pi / 2, math.pi / 2)
            xfood = center[0] + r * math.cos(teta) * math.cos(phi)
            yfood = center[1] - r * math.sin(teta)
            if phi <= math.pi:
                if not collis((xfood, yfood), pointsArray, True, 5)[0]:
                    possib = random.random()
                    if possib < 0.2: typefood = "medved"
                    elif possib < 0.4: typefood = "vodka"
                    else: typefood = "usual"
                    return xfood, yfood, True, typefood
            else:
                if not collis((xfood, yfood), pointsArray, False, 5)[0]:
                    possib = random.random()
                    if possib < 0.2: typefood = "medved"
                    elif possib < 0.4: typefood = "vodka"
                    else: typefood = "usual"
                    return xfood, yfood, False, typefood

def foodgen():
    foodArray.append(Food())
    foodArray.append(newCor(Food.copy(foodArray[-1]), (math.sqrt(3) / 2, 0.5), 15))
    foodArray.append(newCor(Food.copy(foodArray[-2]), (-math.sqrt(3) / 2, 0.5), 15))
    foodArray.append(newCor(Food.copy(foodArray[-3]), (-1, 0), 15))
    foodArray.pop(-4)

def gradient(cor=center, r=r, cenCol=CENCOL, rimCol=RIMCOL, delta=int(r / 2)):
    for i in range(delta):
        pygame.draw.circle(screen, (rimCol[0] + (cenCol[0] - rimCol[0]) / delta * i, rimCol[1] + (cenCol[1] - rimCol[1]) / delta * i, rimCol[2] + (cenCol[2] - rimCol[2]) / delta * i), cor, r - int(r / delta * i))

def arcsin(dest):
    yg = math.asin(-dest[1])
    if dest[0] < 0 and dest[1] <= 0 or dest[0] < 0 and dest[1] > 0:
        yg = math.pi - yg
    elif dest[0] > 0 and dest[1] < 0:
        yg = 2 * math.pi + yg
    return yg

def medveddir(dir, a):
    alph = random.uniform(-a, a)
    return (math.cos(arcsin(dest) + alph), -math.sin(arcsin(dest) + alph))

def drawmouse(point, color, vis, r=10):
    if vis:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r)
        pygame.draw.circle(screen, BLACK, [int(point[0]), int(point[1])], r, 1)
    else:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r, 1)
        #pygame.draw.circle(screen, WHITE, [int(point[0]), int(point[1])], 10, 1)

def drawfield():
    screen.fill(GROUND)
    gradient()

    for piece in foodArray:
        if piece.vis == False:
            drawmouse((piece.x, piece.y), piece.color, piece.vis)

    for i in range(0, len(pointsArray) - 1, 2):
        if not pointsArray[i].vis:
            drawmouse((pointsArray[i].x, pointsArray[i].y), FLAG[i % 3], pointsArray[i].vis, 6)

    for i in range(0, len(pointsArray) - 1, 2):
        if pointsArray[i].vis:
            drawmouse((pointsArray[i].x, pointsArray[i].y), FLAG[i % 3], pointsArray[i].vis, 6)

    for piece in foodArray:
        if piece.vis == True:
            #screen.blit(fontscore.render(piece.type, True, HEAD), (piece.x, piece.y))
            drawmouse((piece.x, piece.y), piece.color, piece.vis)

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

def go():
    global score, pointsArray, foodArray, q, dest, snake_len, done, v, step, vodkaTimer, medvedTimer
    # changes snake coordinates
    for point in pointsArray:
        newCor(point, dest, step)

    # changes food coordinates
    for piece in foodArray:
        newCor(piece, dest, step)

    # collision checking
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 7)], True, 3)[0]:
        done = True
    foodcol = collis((center[0], center[1]), foodArray, True, 10)
    if foodcol[0]: # eating
        v = v0
        foodArray.remove(foodcol[1])
        if foodcol[1].type == "medved":
            dest = medveddir(dest, 3 * math.pi / 4)
            medvedTimer = Timer(0.2)
            vodkaTimer = None
        elif foodcol[1].type == "vodka":
            vodkaTimer = Timer(random.uniform(4, 8))
        score += foodcol[1].scr
        snake_len += grow
        if len(foodArray) <= 6:
            foodgen()

    # checking if snake is growing, then deleting the first point
    if len(pointsArray) == snake_len: pointsArray.pop(0)

    # drawing snake and food
    screen.fill(GROUND)
    gradient()
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    time.sleep(0.02)
    pointsArray.append(Point(center[0], center[1], True))
    drawfield()
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)
    if vodkaTimer != None and Timer.ison(vodkaTimer):
        screen.blit(fontscore.render('Vodka: ' + str(int((-time.time() + vodkaTimer.op + vodkaTimer.long) * 100) / 100), True, RED), (center[0] - 50, 10))
    writescore()
    pygame.display.flip()

screen.fill(GROUND)
gradient()
pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)

#food(5)
for i in range(3): foodgen()
drawfield()
#time.sleep(2)
writescore()

pygame.display.flip()

#time.sleep(3)
done = False
q = (center[0], center[1])
op = time.time()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if medvedTimer != None:
        if not Timer.ison(medvedTimer):
            medvedTimer = None
    else:
        keystate = pygame.key.get_pressed()
        if keystate[13] != 0:
            pointsArray.append(Point(center[0], center[1], True))
            snake_len = 10
            screen.fill(GROUND)
            gradient()
            pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
            pygame.draw.circle(screen, HEAD, [center[0], center[1]], 2)
            pygame.display.flip()
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

    if vodkaTimer != None:
        if Timer.ison(vodkaTimer):
            dest = medveddir(dest, math.pi / 10)
        else:
            vodkaTimer = None

    ed = time.time()
    step = v * (ed - op)
    op = ed
    if step != 0:
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
f = open("russia/records.txt", 'w')
f.write(str(best))
f.close()
time.sleep(2)

#pygame.quit()
