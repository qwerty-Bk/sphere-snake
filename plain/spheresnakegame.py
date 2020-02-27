
import random
import pygame
import math
import time

def spheremain():
    pygame.init()

    fontlose = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 50)
    fontscore = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 15)
    GROUND =(250, 255, 235)
    PLANET =(230, 240, 215)
    CENCOL =(250, 255, 230)
    RIMCOL =(175, 195, 155)
    BLACK = (  0,  30,   0)
    WHITE = (225, 255, 225)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 200,   0)
    LIGHT = (200, 255, 200)
    RED =   (255,   0,   0)
    PINK =  (255, 200, 200)
    SUNNY = (255, 255, 200)
    YELLOW =(200, 200,   0)
    GOL =   (200, 200, 255)
    SNAKET= (105, 155,  50)
    SNAKEF= (170, 220, 115)
    #SNAKEF= ( 50,  90,  30)
    HEAD =  ( 95, 130,  15)
    #FOODT = (255, 150,   0)
    FOODF = (255, 210, 110)
    FOODF = (140,   80, 10)

    v = 100
    r = 250
    size = [600, 600]
    center = [size[0] // 2, size[1] // 2]
    screen = pygame.display.set_mode(size)
    pointsArrayTrue = [[center[0], center[1], 0]]
    pointsArrayFalse = []
    foodTrue = []
    foodFalse = []
    snake_len = 10
    grow = 10
    score = 0
    best = 0

    try:
        f = open("plain/records.txt")
        for line in f:
            best = int(line)
    except FileNotFoundError:
        f = open("plain/records.txt", 'x')
    f.close()

    def gradient(cor, r, cenCol, rimCol, delta = int(r / 2)):
        for i in range(delta):
            pygame.draw.circle(screen, (rimCol[0] + (cenCol[0] - rimCol[0]) / delta * i, rimCol[1] + (cenCol[1] - rimCol[1]) / delta * i, rimCol[2] + (cenCol[2] - rimCol[2]) / delta * i), cor, r - int(r / delta * i))

    def collis(point, pat, delta):
        for i in range(0, len(pat)):
            if point[0] < pat[i][0] + delta and point[0] > pat[i][0] - delta and point[1] < pat[i][1] + delta and point[1] > pat[i][1] - delta:
                return (True, pat[i])
        return (False, None)

    def newTrue(pati): # возвращает измененные координаты и true/false на перекидку в невидимые
        change = False
        ri = math.sqrt((pati[0] - center[0]) ** 2 + (pati[1] - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (pati[0] - center[0]) + (q[1] - center[1]) * (pati[1] - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = math.acos(tcos)
            r0 = math.sqrt(r ** 2 - ri ** 2 * math.sin(a) ** 2)
            alph = math.asin(step / r)
            if r0 == 0:
                return pati, change
            tcos = ri * math.cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= math.pi - math.acos(tcos):
                if dest[0] + dest[1] == 1: ro = ri * math.cos(a) - r0 * math.cos(alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) + alph)
                pati[0] -= dest[0] * abs(ro)
                pati[1] -= dest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) + r0 * math.cos(math.pi - alph - math.acos(tcos))
                pati[0] -= dest[0] * ro
                pati[1] -= dest[1] * ro
                change = True
        else:
            pati[0] -= step * dest[0]
            pati[1] -= step * dest[1]
        return pati, change

    def newFalse(pafi):
        change = False
        ri = math.sqrt((pafi[0] - center[0]) ** 2 + (pafi[1] - center[1]) ** 2)
        if ri != 0:
            tcos = ((q[0] - center[0]) * (pafi[0] - center[0]) + (q[1] - center[1]) * (pafi[1] - center[1])) / step / ri
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            a = math.acos(tcos)
            r0 = math.sqrt(r ** 2 - ri ** 2 * math.sin(a) ** 2)
            alph = math.asin(step / r)
            if r0 == 0:
                return pafi, change
            tcos = ri * math.cos(a) / r0
            if tcos < -1: tcos = -1
            elif tcos > 1: tcos = 1
            if alph <= math.acos(tcos):
                if dest[0] + dest[1] == 1: ro = -ri * math.cos(a) + r0 * math.cos(-alph + math.acos(tcos))
                else: ro = ri * math.cos(a) - r0 * math.cos(-alph + math.acos(tcos))
                pafi[0] += dest[0] * abs(ro)
                pafi[1] += dest[1] * abs(ro)
            else:
                ro = ri * math.cos(a) - r0 * math.cos(math.acos(tcos) - alph)
                pafi[0] -= dest[0] * ro
                pafi[1] -= dest[1] * ro
                change = True
        else:
            pafi[0] += step * dest[0]
            pafi[1] += step * dest[1]
        return pafi, change

    def food(foodTrue = foodTrue, foodFalse = foodFalse, pointsArrayTrue = pointsArrayTrue, pointsArrayFalse = pointsArrayFalse):
        phi = random.random() * 2 * math.pi
        teta = random.random() * math.pi - math.pi / 2
        xfood = center[0] + r * math.cos(teta) * math.cos(phi)
        yfood = center[1] - r * math.sin(teta)
        colorfood = (random.randint(0, 105), random.randint(0, 105), random.randint(0, 105))
        if phi <= math.pi:
            if collis((xfood, yfood), pointsArrayTrue, 5)[0]:
                food()
            else:
                foodTrue.append([xfood, yfood, colorfood])
        else:
            if collis((xfood, yfood), pointsArrayFalse, 5)[0]:
                food()
            else:
                foodFalse.append([xfood, yfood, colorfood])

    def drawfoodT(foodTrue = foodTrue):
        for piece in foodTrue:
            pygame.draw.circle(screen, piece[2], [int(piece[0]), int(piece[1])], 10)
            pygame.draw.circle(screen, BLACK, [int(piece[0]), int(piece[1])], 10, 1)

    def drawfoodF(foodFalse = foodFalse):
        for piece in foodFalse:
            pygame.draw.circle(screen, (piece[2][0] + 150, piece[2][1] + 150, piece[2][2] + 150), [int(piece[0]), int(piece[1])], 10)
            pygame.draw.circle(screen, WHITE, [int(piece[0]), int(piece[1])], 10, 1)

    def writescore(score):
        screen.blit(fontscore.render('score: ' + str(int(score)), True, BLACK), (10, 10))
        screen.blit(fontscore.render('best score: ' + str(best), True, BLACK), (10, 25))

    def go(q, dest, pointsArrayTrue, pointsArrayFalse, foodTrue, foodFalse, snake_len, done, score):
        # изменение координат змеи
        tbdTrue = []
        for i in range(len(pointsArrayTrue)):
            pointsArrayTrue[i], change = newTrue(pointsArrayTrue[i])
            if change: tbdTrue.append(pointsArrayTrue[i])

        tbdFalse = []
        for i in range(len(pointsArrayFalse)):
            pointsArrayFalse[i], change = newFalse(pointsArrayFalse[i])
            if change: tbdFalse.append(pointsArrayFalse[i])

        pointsArrayTrue += tbdFalse
        pointsArrayFalse += tbdTrue
        for i in tbdTrue: pointsArrayTrue.remove(i)
        for i in tbdFalse: pointsArrayFalse.remove(i)

        # изменение координат еды
        tbdTrue = []
        for i in range(len(foodTrue)):
            foodTrue[i], change = newTrue(foodTrue[i])
            if change: tbdTrue.append(foodTrue[i])

        tbdFalse = []
        for i in range(len(foodFalse)):
            foodFalse[i], change = newFalse(foodFalse[i])
            if change: tbdFalse.append(foodFalse[i])

        foodTrue += tbdFalse
        foodFalse += tbdTrue
        for i in tbdTrue: foodTrue.remove(i)
        for i in tbdFalse: foodFalse.remove(i)

        # проверка на столкновения
        scorebaf = 0
        if collis((center[0], center[1]), pointsArrayTrue[:(len(pointsArrayTrue) - 9)], 2)[0]:
            done = True
        foodcol = collis((center[0], center[1]), foodTrue, 10)
        if foodcol[0]: # eating
            foodTrue.remove(foodcol[1])
            scorebaf = sum(foodcol[1][2]) / 30
            snake_len += grow
            food()

        # отрисовка змеи + еды
        screen.fill(GROUND)
        gradient(center, r, CENCOL, RIMCOL)
        pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
        time.sleep(0.02)

        drawfoodF()

        pointtbd = None
        for point in pointsArrayFalse:
            if len(pointsArrayTrue) + len(pointsArrayFalse) < snake_len:
                point[2] += 1
                pygame.draw.circle(screen, SNAKEF, [int(point[0]), int(point[1])], 5)
            elif len(pointsArrayTrue) + len(pointsArrayFalse) == snake_len:
                point[2] += 1
                if point[2] == snake_len: pointtbd = point
                else: pygame.draw.circle(screen, SNAKEF, [int(point[0]), int(point[1])], 5)
            else:
                print('ERROR!!!')
                exit()
        if pointtbd != None:
            pointsArrayFalse.remove(pointtbd)

        drawfoodT()

        pointtbd = None
        for point in pointsArrayTrue:
            if len(pointsArrayTrue) + len(pointsArrayFalse) < snake_len:
                point[2] += 1
                pygame.draw.circle(screen, SNAKET, [int(point[0]), int(point[1])], 5)
            elif len(pointsArrayTrue) + len(pointsArrayFalse) == snake_len:
                point[2] += 1
                if point[2] == snake_len: pointtbd = point
                else: pygame.draw.circle(screen, SNAKET, [int(point[0]), int(point[1])], 5)
            else:
                print("ERROR!!!")
                exit()
        if pointtbd != None:
            pointsArrayTrue.remove(pointtbd)
        pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)
        pointsArrayTrue.append([center[0], center[1], 0])
        writescore(score)
        pygame.display.flip()
        return snake_len, done, scorebaf

    screen.fill(GROUND)

    gradient(center, r, CENCOL, RIMCOL)
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
    pygame.draw.circle(screen, HEAD, [center[0], center[1]], 10)

    for i in range(5): food()
    drawfoodF()
    drawfoodT()
    writescore(score)

    pygame.display.flip()

    done = False
    dest = (0, -1)
    q = (center[0], center[1])
    op = time.time()

    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
        keystate = pygame.key.get_pressed()
        if keystate[13] != 0:
            pointsArrayTrue = [[center[0], center[1], 0]]
            pointsArrayFalse = []
            snake_len = 10
            screen.fill(GROUND)
            gradient(center, r, CENCOL, RIMCOL)
            pygame.draw.circle(screen, HEAD, [center[0], center[1]], r, 1)
            pygame.draw.circle(screen, HEAD, [center[0], center[1]], 2)
            pygame.display.flip()
        if keystate[pygame.K_UP]:
            if dest != (0, 1):
                dest = (0, -1)
        if keystate[pygame.K_DOWN]:
            if dest != (0, -1):
                dest = (0, 1)
        if keystate[pygame.K_RIGHT]:
            if dest != (-1, 0):
                dest = (1, 0)
        if keystate[pygame.K_LEFT]:
            if dest != (1, 0):
                dest = (-1, 0)

        ed = time.time()
        step = v * (ed - op)
        op = ed
        if step != 0:

            q = (center[0] + dest[0] * step, center[1] + dest[1] * step)
            snake_len, done, scorebaf = go(q, dest, pointsArrayTrue, pointsArrayFalse, foodTrue, foodFalse, snake_len, done, score)
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
    f = open("plain/records.txt", 'w')
    f.write(str(best))
    f.close()
    time.sleep(2)

spheremain()
    # pygame.quit()
