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
HEAD =  BLACK
GERMAN =WHITE
GERNO = BLACK
FLAG = [(255, 255, 0), (255, 180, 0), BLACK]

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

environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (650 - center[0], 350 - center[1])
pygame.init()

screen = pygame.display.set_mode(size)
fontlose = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 50)
fontscore = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 15)

# getting best score
try:
    f = open("germany/germrecords.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("germany/germrecords.txt", 'x')
f.close()

class Point:

    def __init__(self, x, y, vis):
        self.x = x
        self.y = y
        self.vis = vis
        self.speed = v0

class Germish():

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.dir = Germish.finddir(self)
        self.color = GERMAN
        self.speed = random.uniform(0.75 * v0, v0)
        self.scr = random.uniform(1, 10)

    def finddir(piece): #AAAAAAAAAAAAAAAAAAAAA
        dir = (-(center[0] - piece.x) / math.sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2), -(center[1] - piece.y) / math.sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2))
        return (dir[0], dir[1])

class Gerno():

    def __init__(self, place):
        self.x, self.y, self.vis = place
        self.dir = Gerno.finddir(self)
        self.color = GERNO
        self.speed = random.uniform(0.15 * v0, 0.35 * v0)
        self.scr = random.uniform(1, 10)

    def finddir(piece): #AAAAAAAAAAAAAAAAAAAAA
        dir = ((center[0] - piece.x) / math.sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2), (center[1] - piece.y) / math.sqrt((center[0] - piece.x) ** 2 + (center[1] - piece.y) ** 2))
        return (dir[0], dir[1])

def food():
    freeCor = findcor()
    possib = random.random()
    if possib < 0.5:
        foodArray.append(Germish(freeCor))
    else:
        foodArray.append(Gerno(freeCor))

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

def drawmouse(point, color, vis, r=10):
    if vis:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r)
        pygame.draw.circle(screen, BLACK, [int(point[0]), int(point[1])], r, 1)
    else:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], r, 1)

def drawfield():

    screen.fill(GROUND)
    gradient()
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    time.sleep(0.02)

    for piece in foodArray:
        if piece.vis == False:
            drawmouse((piece.x, piece.y), piece.color, piece.vis)

    for i in range(0, len(pointsArray) - 1, 2):
        #if i > 1: pointsArray[i].color = pointsArray[i - 1].color
        if not pointsArray[i].vis:
            drawmouse((int(pointsArray[i].x), int(pointsArray[i].y)), FLAG[i % 3], pointsArray[i].vis, 7)
        #if not pointsArray[i].vis:
        #    pygame.draw.circle(screen, SNAKEF, [int(pointsArray[i].x), int(pointsArray[i].y)], 6)

    for i in range(0, len(pointsArray) - 1, 2):
        if pointsArray[i].vis:
            drawmouse((int(pointsArray[i].x), int(pointsArray[i].y)), FLAG[i % 3], pointsArray[i].vis, 7)
        #if pointsArray[i].vis:
        #    pygame.draw.circle(screen, SNAKET, [int(pointsArray[i].x), int(pointsArray[i].y)], 6)

    for piece in foodArray:
        if piece.vis == True:
            drawmouse((piece.x, piece.y), piece.color, piece.vis)

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

def go():
    global score, done, snake_len
    # changes snake coordinates
    for point in pointsArray:
        #print('newcor for', point.x, point.y)
        newCor(point, dest)

    # changes food coordinates
    for piece in foodArray:
        newCor(piece, piece.dir, piece.speed)
        newCor(piece, dest)
        if type(piece) == Germish:
            piece.dir = Germish.finddir(piece)
        elif type(piece) == Gerno:
            piece.dir = Gerno.finddir(piece)

    # collision checking
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 4)], True, 5)[0]:
        done = True
    foodcol = collis((center[0], center[1]), foodArray, True, 10)
    if foodcol[0]: # eating
        foodArray.remove(foodcol[1])
        score += foodcol[1].scr
        snake_len += grow
        food()

    # checking if snake is growing, then deleting the first point
    if len(pointsArray) == snake_len: pointsArray.pop(0)
    pointsArray.append(Point(center[0], center[1], True))

    # drawing snake and food
    drawfield()

for i in range(5):
    food()

done = False
q = (center[0], center[1])
op = time.time()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keystate = pygame.key.get_pressed()
    if keystate[13] != 0:
        pointsArray = [Point(center[0], center[1], True)]
        snake_len = 10
        score = 0
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
    dt = ed - op
    op = ed
    if dt != 0:
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
f = open("germany/germrecords.txt", 'w')
f.write(str(best))
f.close()
time.sleep(2)

# pygame.quit()
