import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1550, 680))
ball_count = 8  #количество шаров на экране
score = 0 #счет очков

#код цвета в rgb
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# массивы для шаров
x = [0 for i in range(ball_count)]
y = [0 for i in range(ball_count)]
r = [0 for i in range(ball_count)]
vx = [0 for i in range(ball_count)]
vy = [0 for i in range(ball_count)]
color = [0 for i in range(ball_count)]

def new_ball(i: int):
    '''рисует новый шарик с номером i'''
    x[i] = randint(100, 1450)
    y[i] = randint(100, 580)
    r[i] = randint(10, 100)
    vx[i] = randint(-7, 7)
    vy[i] = randint(-7, 7)
    color[i] = COLORS[randint(0, 5)]
    circle(screen, color[i], (x[i], y[i]), r[i])

def move_ball(i: int):
    '''перемещает шарик по экрану '''

    circle(screen, BLACK, (x[i], y[i]), r[i])
    if (x[i] - r[i]) <= 0 or (x[i] + r[i]) >= 1550:
        vx[i] = -vx[i]
    if (y[i] - r[i]) <= 0 or (y[i] + r[i]) >= 680:
        vy[i] = -vy[i]
    x[i] += vx[i]
    y[i] += vy[i]
    circle(screen, color[i], (x[i], y[i]), r[i])

def click(event):

    global score

    for i in range(ball_count):
        if (event.pos[0] - x[i])**2 + (event.pos[1] - y[i])**2 <= r[i]**2:
            circle(screen, BLACK, (x[i], y[i]), r[i])
            new_ball(i)
            score+=1

def score_point(score: int):
    '''выводит на экран количество набранных очков '''

    f = pygame.font.Font(None, 36)
    text = f.render('Score: ' +str(score-1), 1, (0, 0, 0))
    screen.blit(text, (24, 18))
    text = f.render('Score: ' +str(score), 1, (180, 0, 0))
    screen.blit(text, (24, 18))

# основная программа
pygame.display.update()
clock = pygame.time.Clock()
finished = False
for i in range(ball_count):
    new_ball(i)

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    for i in range(ball_count):
        move_ball(i)
    score_point(score)
    pygame.display.update()

pygame.quit()
