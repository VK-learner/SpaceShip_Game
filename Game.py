# Space Invaders:
import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# Background image.
background = pygame.image.load('background.jpg')

# Background music
mixer.music.load('Bmusic.wav')
mixer.music.play(-1)# this is used to continuously loop the music.

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship2.png')
playerX = 370
playerY = 480
playerX_change = 0

# Create a list of Enemies to get multiple enemies.
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 # increase the number of enemies.

# Use for loop to get 6 enemies.
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))  # 800 replace by 735 since last statement
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)  # enemy initial speed before hitting the wall.
    enemyY_change.append(60)  # enemy movement downside to attack the spaceship

# Bullet
# Ready : You can't see the bullet on the screen.
# Fire : The bullet is currently moving.
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  # Because our spaceship is at 480 pixel i.e, see line 21
bulletX_change = 0
bulletY_change = 6  # Bullet speed
bullet_state = "ready"

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10# X coordinate and Y coordinate on which we want the score to appear.
textY = 10

# TODO:2  Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

# create a function to show font.
def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))# 1st render the score then blit it.
    screen.blit(score,(x,y))# to show on screen the score

# TODO:3 game_over_text() function
def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):# specify i value
    screen.blit(enemyImg[i], (x, y))


# Creating a bullet function.
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))# Bullet position


# Create a collision function using distance formula (distance bw spaceship and enemy)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # adding the background image.
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Is keystroke is pressed check whether its right or left.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2  # Spaceship L-speed
            if event.key == pygame.K_RIGHT:
                playerX_change = 2  # Spaceship R-speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Bullet sound while shooting
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries spaceship so it doesn't go out.
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    # when the above for loop runs to create multiple enemies
    # the while loop not get to which enemy it has to cl hence we have to mention enemy by indexing.
    # hence we create another for loop to iterate it and use indexing i.
    for  i in  range(num_of_enemies):
        # TODO:1 Game Over condition
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1  # enemy speed after hitting the wall
            enemyY[i] += enemyY_change[i]  # Enemy moves downside when hit by wall.
        elif enemyX[i] >= 768:
            enemyX_change[i] = -1  # enemy speed after hitting the wall
            enemyY[i] += enemyY_change[i]  # Enemy moves downside when hit by wall.

        # place the collision inside this while loop and place inside the for loop because it should work for
        # all enemies when they get hit by the bullet. NOTE: Use Indexing i here also.
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')# explosion sound
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score_value) not needed as it is seen on display
            # to make any reappear when hit by a bullet st different location. or to make enemy respawn to his location.
            enemyX[i] = random.randint(0, 735)  # 800 replace by 735 since last statement
            enemyY[i] = random.randint(50, 150)

        # paste the enemy(enemyX,enemyY) here
        enemy(enemyX[i],enemyY[i],i)# i is used to specify to which enemy collision has happened.

    # Bullet Movement.

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        # fire_bullet(playerX,bulletY)
        fire_bullet(bulletX, bulletY)  # replace playerX by bulletX as per 2
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
