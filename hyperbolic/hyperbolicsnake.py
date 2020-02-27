
import random
import pygame
import math
import time

pygame.init()

fontlose = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 50)
fontscore = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 15)
GROUND =(250, 255, 235)
PLANET =( 45,  65,  30)
CENCOL =(250, 255, 230)
RIMCOL =(195, 205, 175)
WHITE = (225, 255, 225)
BLUE =  (  0,   0, 255)
GREEN = (  0, 200,   0)
LIGHT = (200, 255, 200)
RED =   (255,   0,   0)
PINK =  (255, 200, 200)
SUNNY = (255, 255, 200)
YELLOW =(200, 200,   0)
GOL =   (200, 200, 255)
SNAKE = (105, 155,  50)
HEAD =  ( 95, 130,  15)

v = 100
r = 250
size = [600, 600]
center = [size[0] // 2, size[1] // 2]
maincenter = list(center)
circlecenter = list(center)
screen = pygame.display.set_mode(size)
pointsArray = [[center[0], center[1]]]
food = []
#wall = []
bound = []
#alpha = math.asin(4 / (r - 4))
alphab = math.pi / 3
ro = 240
for i in range(3):
    bound.append([center[0] + math.cos(alphab * i) * ro, center[1] - math.sin(alphab * i) * ro])
#for i in range(int(2 * math.pi / alpha) + 1):
#    wall.append([center[0] + math.cos(alpha * i) * ro, center[1] - math.sin(alpha * i) * ro])
snake_len = 10
grow = 10
score = 0
best = 0
dest = [1, 0]

try:
    f = open("hyperbolic/hyprecords.txt")
    for line in f:
        best = int(line)
except FileNotFoundError:
    f = open("hyperbolic/hyprecords.txt", 'x')
f.close()

def gradient(cor, r, cenCol, rimCol, delta = int(r / 2)):
    for i in range(delta):
        pygame.draw.circle(screen, (rimCol[0] + (cenCol[0] - rimCol[0]) / delta * i, rimCol[1] + (cenCol[1] - rimCol[1]) / delta * i, rimCol[2] + (cenCol[2] - rimCol[2]) / delta * i), cor, r - int(r / delta * i))

def atg(dest):
    if dest[0] >= 0 and dest[1] > 0:
        #print('I четверть, return',  math.atan(dest[1] / dest[0]) / math.pi * 180)
        return math.atan(dest[1] / dest[0])
    if dest[0] < 0 and dest[1] >= 0:
        #print('II четверть, return', (math.pi + math.atan(dest[1] / dest[0])) / math.pi * 180)
        return math.pi + math.atan(dest[1] / dest[0])
    if dest[0] <= 0 and dest[1] < 0:
        #print('III четверть, return', (math.pi + math.atan(dest[1] / dest[0])) / math.pi * 180)
        return math.pi + math.atan(dest[1] / dest[0])
    #print('IV четверть, return', (2 * math.pi + math.atan(dest[1] / dest[0])) / math.pi * 180)
    return 2 * math.pi + math.atan(dest[1] / dest[0])

def collis(point, pa, delta):
    for i in range(0, len(pa)):
        if point[0] < pa[i][0] + delta and point[0] > pa[i][0] - delta and point[1] < pa[i][1] + delta and point[1] > pa[i][1] - delta:
            return (True, pa[i])
    return (False, None)

def runaway(point, circlecenter, ro):
    if (circlecenter[0] - point[0]) ** 2 + (circlecenter[1] - point[1]) ** 2 > (ro) ** 2:
        #time.sleep(0.07)
        return True
    return False

def hyp(x, v):
    return ( ((1 + 2 * (v[0] * x[0] + v[1] * x[1]) + x[0] ** 2 + x[1] ** 2) * v[0] + (1 - v[0] ** 2 - v[1] ** 2) * x[0]) / (1 + 2 * (v[0] * x[0] + v[1] * x[1]) + (x[0] ** 2 + x[1] ** 2) * (v[0] ** 2 + v[1] ** 2)), ((1 + 2 * (v[0] * x[0] + v[1] * x[1]) + x[0] ** 2 + x[1] ** 2) * v[1] + (1 - v[0] ** 2 - v[1] ** 2) * x[1]) / (1 + 2 * (v[0] * x[0] + v[1] * x[1]) + (x[0] ** 2 + x[1] ** 2) * (v[0] ** 2 + v[1] ** 2)) )

def foodgen(ro, circlecenter = circlecenter, food = food, pointsArray = pointsArray):
    phi = random.random() * 2 * math.pi
    rad = random.random() * ro
    xfood = circlecenter[0] + rad * math.cos(phi)
    yfood = circlecenter[1] - rad * math.sin(phi)
    if collis((xfood, yfood), pointsArray, 10)[0]:
        foodgen(ro)
    else:
        colorfood = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        food.append([xfood, yfood, colorfood])

def drawfood(food = food):
    for piece in food:
        pygame.draw.circle(screen, piece[2], [int(piece[0]), int(piece[1])], 10)
        pygame.draw.circle(screen, PLANET, [int(piece[0]), int(piece[1])], 10, 1)

#def drawwall(wall = wall):
#    pygame.draw.aalines(screen, PLANET, True, wall)

def drawbound(ro, circlecenter = circlecenter):
    pygame.draw.circle(screen, PLANET, (int(circlecenter[0]), int(circlecenter[1])), int(ro), 3)

def writescore(score):
    screen.blit(fontscore.render('score: ' + str(int(score)), True, PLANET), (10, 10))
    screen.blit(fontscore.render('best score: ' + str(best), True, PLANET), (10, 25))

def go(q, step, pointsArray, food, snake_len, done, score, dest):
    #global dest
    #изменение координат змеи и основного центра
    newdest = [dest[0] * step / r, dest[1] * step / r]
    for point in pointsArray:
        point[0], point[1] = center[0] + r * hyp([(point[0] - center[0]) / r, (point[1] - center[1]) / r], newdest)[0], center[1] + r * hyp([(point[0] - center[0]) / r, (point[1] - center[1]) / r], newdest)[1]
    maincenter[0], maincenter[1] = center[0] + r * hyp([(maincenter[0] - center[0]) / r, (maincenter[1] - center[1]) / r], newdest)[0], center[1] + r * hyp([(maincenter[0] - center[0]) / r, (maincenter[1] - center[1]) / r], newdest)[1]

    #изменение координат еды
    for piece in food:
        piece[0], piece[1] = center[0] + r * hyp([(piece[0] - center[0]) / r, (piece[1] - center[1]) / r], newdest)[0], center[1] + r * hyp([(piece[0] - center[0]) / r, (piece[1] - center[1]) / r], newdest)[1]

    #изменение координат стены
    #for brick in wall:
    #    brick[0], brick[1] = center[0] + r * hyp([(brick[0] - center[0]) / r, (brick[1] - center[1]) / r], newdest)[0], center[1] + r * hyp([(brick[0] - center[0]) / r, (brick[1] - center[1]) / r], newdest)[1]
    for pillar in bound:
        pillar[0], pillar[1] = center[0] + r * hyp([(pillar[0] - center[0]) / r, (pillar[1] - center[1]) / r], newdest)[0], center[1] + r * hyp([(pillar[0] - center[0]) / r, (pillar[1] - center[1]) / r], newdest)[1]
    x1, x2, x3 = bound[0][0], bound[1][0], bound[2][0]
    y1, y2, y3 = bound[0][1], bound[1][1], bound[2][1]
    ma, mb = (y2 - y1) / (x2 - x1), (y3 - y2) / (x3 - x2)
    circlecenter[0] = (ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)) / 2 / (mb - ma)
    circlecenter[1] = (x1 + x2 - 2 * circlecenter[0]) / 2 / ma + (y1 + y2) / 2
    ro = math.sqrt((x1 - circlecenter[0]) ** 2 + (y1 - circlecenter[1]) ** 2)

    #проверка на столкновения
    scorebaf = 0
    if collis((center[0], center[1]), pointsArray[:(len(pointsArray) - 2)], 4)[0]:
        done = True
    if runaway(center, circlecenter, ro):
        vec = [center[0] - circlecenter[0], center[1] - circlecenter[1]]
        aleph = math.acos((-dest[0] * vec[0] + -dest[1] * vec[1]) / math.sqrt(vec[0] ** 2 + vec[1] ** 2))
        #print('aleph with dest, vec with atg(vec):', aleph / math.pi * 180, dest, vec, atg([vec[0], -vec[1]]) / math.pi * 180)
        beta = 0
        if atg((dest[0] / 10000 + vec[0] + 0.0000000001, -vec[1] - dest[1] / 10000)) < atg((vec[0] + 0.0000000001, -vec[1])):
            #print("по часовой")
            beta = atg([dest[0] + 0.0000000001, -dest[1]]) + math.pi - 2 * aleph
        else:
            #print('против часовой')
            beta = atg([dest[0] + 0.0000000001, -dest[1]]) + math.pi + 2 * aleph
        #print('beta for new dest:', beta / math.pi * 180)
        dest = [math.cos(beta), -math.sin(beta)]
        #print('new dest:', dest)

    foodcol = collis((center[0], center[1]), food, 20)
    if foodcol[0]: # eating
        food.remove(foodcol[1])
        scorebaf = sum(foodcol[1][2]) / 30
        snake_len += grow
        foodgen(ro)

    # отрисовка змеи + еды
    screen.fill(GROUND)
    gradient(center, r, CENCOL, RIMCOL)
    #drawwall()
    drawbound(ro)
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    pygame.draw.circle(screen, PLANET, [int(maincenter[0]), int(maincenter[1])], 2)
    time.sleep(0.02)

    if len(pointsArray) == snake_len: # змейка не растет, надо удалить точку
        pointsArray.remove(pointsArray[0])
        #pointsArray = pointsArray[:-1]

    for point in pointsArray:
        pygame.draw.circle(screen, SNAKE, (int(point[0]), int(point[1])), 5)

    pointsArray.append([center[0], center[1]])
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)

    drawfood()

    writescore(score)
    pygame.display.flip()
    return snake_len, done, scorebaf, ro, dest

screen.fill(GROUND)

gradient(center, r, CENCOL, RIMCOL)
pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)

for i in range(5): foodgen(ro)
drawfood()
#drawwall()
drawbound(ro)
writescore(score)

pygame.display.flip()
done = False
q = (center[0], center[1])
op = time.time()

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    keystate = pygame.key.get_pressed()
    if keystate[13] != 0:
        pointsArray = [[center[0], center[1], 0]]
        snake_len = 10
        score = 0
        screen.fill(GROUND)
        gradient(center, r, CENCOL, RIMCOL)
        pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
        pygame.draw.circle(screen, HEAD, [center[0], center[1]], 2)
        pygame.display.flip()
    if keystate[pygame.K_UP]:
        if dest != [0, -1]:
            dest = [0, 1]
    if keystate[pygame.K_DOWN]:
        if dest != [0, 1]:
            dest = [0, -1]
    if keystate[pygame.K_RIGHT]:
        if dest != [1, 0]:
            dest = [-1, 0]
    if keystate[pygame.K_LEFT]:
        if dest != [-1, 0]:
            dest = [1, 0]
    ed = time.time()
    step = v * (ed - op)
    op = ed
    if step != 0:
        q = (center[0] + dest[0] * step, center[1] + dest[1] * step)
        snake_len, done, scorebaf, ro, dest = go(q, step, pointsArray, food, snake_len, done, score, dest)
        score += scorebaf
if score > best:
    best = int(score)
    screen.fill(LIGHT)
    screen.blit(fontlose.render('NEW HIGH SCORE', True, GREEN), (65, 200))
else:
    screen.fill(PINK)
    screen.blit(fontlose.render('YOU HAVE LOST', True, RED), (85, 200))
writescore(score)
pygame.display.flip()
f = open("hyperbolic/hyprecords.txt", 'w')
f.write(str(best))
f.close()
time.sleep(2)

# pygame.quit()
