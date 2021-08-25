import pygame
import random
import math
from pygame import mixer

# To initialize a game and create an object screen
pygame.init()

screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('backImage.png')

# add background soud
mixer.music.load('background_music.wav')
mixer.music.play(-1)

# Icon and name
pygame.display.set_caption("Alien Invasion")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# adding spaceship
image = pygame.image.load('images/space-ship-icon.png')
imageX = 370
imageY = 480
imageX_displace = 0

# adding enemy
enemy = []
enemyX = []
enemyY = []
enemyX_displace = []
enemyY_displace = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemy.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_displace.append(0.3)
    enemyY_displace.append(40)

# adding bullet
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_displace = 0
bulletY_displace = 5
bullet_state = "Ready"

# Score Board
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    score = over_font.render('GAME OVER :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (200, 250))


def Player(x, y):
    screen.blit(image, (x, y))


def Enemy(x, y, i):
    screen.blit(enemy[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Start the main loop for the game.

running = True
while running:
    screen.fill((0, 210, 210))
    # background image
    screen.blit(background, (0, 0))
    # Watch for keyboard and mouse events.
    # Event is an action performed by user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                imageX_displace = -0.3

            if event.key == pygame.K_RIGHT:
                imageX_displace = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    play = mixer.Sound('laser.wav')
                    play.play()
                    bulletX = imageX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                imageX_displace = 0
    # Checking boundaries

    imageX += imageX_displace
    if imageX <= 0:
        imageX = 0
    elif imageX >= 700:
        imageX = 700

    # enemy movement
    for i in range(num_of_enemy):
        if enemyY[i] > 200:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_displace[i]
        if enemyX[i] <= 0:
            enemyX_displace[i] = 0.4
            enemyY[i] += enemyY_displace[i]
        elif enemyX[i] >= 736:
            enemyX_displace[i] = -0.4
            enemyY[i] += enemyY_displace[i]

        #Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collide = mixer.Sound('explosion.wav')
            collide.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        Enemy(enemyX[i], enemyY[i], i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(imageX, bulletY)
        bulletY -= bulletY_displace

    Player(imageX, imageY)
    show_score(textX, textY)
    # Make the most recently drawn screen visible.
    pygame.display.flip()

