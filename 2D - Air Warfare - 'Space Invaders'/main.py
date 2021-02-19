import pygame
import random
import math
from pygame import mixer

# Initialization, screen creation and icon/title update
pygame.init()
screen = pygame.display.set_mode(size=(800, 600), vsync=1)
pygame.display.set_caption("Air Warfare")
icon = pygame.image.load("img/bomb.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("img/background.png").convert()
mixer.music.load("sfx/background.wav")
mixer.music.play(-1)

# Explotion Image
explosionIcon = pygame.image.load("img/explosion.png")

# Player Image
playerIcon = pygame.image.load("img/jet.png")
playerX = 370
playerY = 450
playerX_change = 0

# Enemies
enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyIcon.append(pygame.image.load("img/flight.png"))
    enemyX.append(random.randint(2, 734))
    enemyY.append(random.randint(25, 75))
    enemyX_change.append(1)
    enemyY_change.append(25)


# Bullet Image
bulletIcon = pygame.image.load("img/bullet.png")
bulletX = 0
bulletY = 450
bulletY_change = 1.75
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("font.otf", 32)
textX = 10
textY = 10

# 'Game over' text
over_font = pygame.font.Font("font.otf", 96)


def player(x, y):
    screen.blit(playerIcon, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletIcon, (x + 16, y + 10))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (150, 225))


def explosion(x, y):
    screen.blit(explosionIcon, (x, y))


def isCollision(x1, y1, x2, y2):
    dist = ((int(x2 - x1))**2 + int(y2 - y1)**2)**0.5
    if dist < 27:
        return True
    return False


# Game Loop
running = True
while running:
    screen.fill((0, 128, 128))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                playerX_change = -1.5
            if event.key == pygame.K_d:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("sfx/gunshot.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Player movement
    if playerX >= 734:
        playerX = 734
    if playerX <= 2:
        playerX = 2
    playerX += playerX_change

    # Enemy movement
    for i in range(num_of_enemies):
        if enemyX[i] >= 734:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 2:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

        # Bullet collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion(enemyX[i], enemyY[i])
            explosion_sound = mixer.Sound("sfx/explosion.wav")
            explosion_sound.play()
            bulletY = 450
            bullet_state = "ready"
            reload_sound = mixer.Sound("sfx/reload.wav")
            reload_sound.play()
            score_value += 1
            enemyX[i] = random.randint(2, 734)
            enemyY[i] = -64

        # Game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            playerIcon = explosionIcon
            explosion_sound = mixer.Sound("sfx/explosion.wav")
            explosion_sound.play(-1)
            break

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= -16:
        bulletY = 450
        bullet_state = "ready"
        reload_sound = mixer.Sound("sfx/reload.wav")
        reload_sound.play()

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Display
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
