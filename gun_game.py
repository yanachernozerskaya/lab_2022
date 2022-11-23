import pygame
import math
import random as rnd
from random import choice


FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = gun.x
        self.y = gun.y
        self.r = 10
        self.color = choice(GAME_COLORS)
        self.tick = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy

        self.vy = self.vy - 4
        if self.y + self.r >= HEIGHT or self.y - self.r <= 0:
            self.vy = -self.vy * 0.5
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.vx = -self.vx * 0.5
        if self.x + self.r >= WIDTH:
            self.x = self.x - abs(self.vx)
        if self.x - self.r <= 0:
            self.x = self.x + abs(self.vx)
        if self.y + self.r >= HEIGHT:
            self.y = self.y - abs(self.vy)
        if self.y - self.r <= 0:
            self.y = self.y + abs(self.vy)
        self.tick += 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

class Gun:
    def __init__(self, screen):
        '''Создает координаты, цвет и другие параметры пушки'''
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + math.cos(self.an) * (20 + self.f2_power/2), self.y + math.sin(self.an)
             * (20 + self.f2_power/2)),
            width=10
        )

    def power_up(self):
        '''Заряжает ружье'''
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Target:
    def __init__(self, screen):
        '''Создает координаты, параметры и очки, которые соответствуют этой цели'''
        self.screen = screen
        self.points = 0
        self.new_target()

    def new_target(self):
        """Новая цель """
        self.x = rnd.randint(60, 740)
        self.y = rnd.randint(60, 540)
        self.r = rnd.randint(2, 50)
        self.color = BLACK
        self.vx = rnd.randint(-100, 100)/10
        self.vy = rnd.randint(-100, 100)/10

    def hit(self, points=1):
        '''Счет увеличивается на 1 при попадании в цель'''
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= 800 or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r >= 600 or self.y - self.r <= 0:
            self.vy = -self.vy

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
targets = [target1, target2]

textfont = pygame.font.SysFont('monospace', 27)

finished = False

while not finished:
    screen.fill(WHITE)
    score = target1.points + target2.points
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
        if b.tick >= 100:
            balls.remove(b)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for target in targets:
        target.move()

    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target):
                target.hit()
                target.new_target()

    gun.power_up()

    text = textfont.render("Score = " + str(score), 1, (0, 0, 0))
    screen.blit(text, (50, 50))

    pygame.display.update()

pygame.quit()