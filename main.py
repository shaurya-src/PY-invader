from math import sqrt
from random import randint

import pygame
from pygame import mixer

# initialize
pygame.init()

# screen
screen = pygame.display.set_mode((900, 600))

# icon and title
icon = pygame.image.load('Assets\\icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')

# background
bg = pygame.image.load('Assets\\bg.png')

# background music
mixer.music.load('Assets\\Sound Effects\\music.mp3')
mixer.music.play(-1)

# score
score_value = 0
font = pygame.font.Font('Assets\\Zdyk Cancer.otf', 32)

t_x = 10
t_y = 10


def show_score(x, y):
    score = font.render('SCORE : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over
font2 = pygame.font.Font('Assets\\Fontix.ttf', 100)


def game_over():
    over_text = font2.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text, (250, 200))


# player
player_img = pygame.image.load('Assets\\player3.png')
p_x = 418
p_y = 480
px_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))  # blit is used to draw


# enemy
enemy_img = []
e_x = []
e_y = []
ex_change = []
ey_change = []

enemies = 6

for _ in range(enemies):
    enemy_img.append(pygame.image.load('Assets\\enemy2.png'))
    e_x.append(randint(0, 836))
    e_y.append(randint(0, 150))
    ex_change.append(2.5)
    ey_change.append(30)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load('Assets\\bullet.png')
b_x = 0
b_y = 480
bx_change = 0
by_change = -4
b_state = 'ready'  # ready(rest)/fire(motion)


def fire_bullet(x, y):
    global b_state
    b_state = 'fire'
    screen.blit(bullet_img, (x + 17, y - 15))


# collision detection
def collision(bx, by, ex, ey):
    c_dist = sqrt((bx - ex) ** 2 + (by - ey) ** 2)

    if c_dist < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:

    # screen fill
    screen.fill((0, 0, 0))
    # pygame.display.update()       # yeh ni karna
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_change = -4
            if event.key == pygame.K_RIGHT:
                px_change = 4
            if event.key == pygame.K_UP:
                if b_state is 'ready':
                    b_sound = mixer.Sound('Assets\\Sound Effects\\shot.wav')
                    b_sound.play()
                    b_x = p_x
                    fire_bullet(b_x, b_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                px_change = 0

    # player movement
    p_x += px_change

    if p_x < 0:
        p_x = 0
    elif p_x > 836:
        p_x = 836

    # enemy movement
    for i in range(enemies):

        if e_y[i] > 430:
            for j in range(enemies):
                e_y[j] = 2000

            game_over()  # Game over text
            break

        e_x[i] += ex_change[i]

        if e_x[i] <= 0:
            ex_change[i] = 2.5
            e_y[i] += ey_change[i]
        elif e_x[i] >= 836:
            ex_change[i] = -2.5
            e_y[i] += ey_change[i]

        # collision check
        is_collided = collision(b_x, b_y, e_x[i], e_y[i])

        if is_collided:
            kill_sound = mixer.Sound('Assets\\Sound Effects\\impact_trim.wav')
            kill_sound.play()
            b_y = 480
            b_state = 'ready'
            score_value += 1
            e_x[i] = randint(0, 836)
            e_y[i] = randint(0, 150)

        enemy(e_x[i], e_y[i], i)

    # bullet movement
    if b_y <= 0:
        b_y = 480
        b_state = 'ready'

    if b_state is 'fire':
        fire_bullet(b_x, b_y)
        b_y += by_change

    player(p_x, p_y)
    show_score(t_x, t_y)
    pygame.display.update()
