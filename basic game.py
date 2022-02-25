# My first pygame project

import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# Shape of the pygame window
WIDTH, HEIGHT = 900, 500
# Create the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")

# Some constants
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
YELLOW = 255, 255, 0

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)
BONUS_YELLOW = pygame.Rect(25, 56, 10, 10)
BONUS_RED = pygame.Rect(550, 79, 10, 10)

# Sounds effects
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)

#How many frames per second
FPS = 100
VEL = 3
BULLET_VEL = 4
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

#Create user defined events for when bullets hits players
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

Y_ANGLE = 90
R_ANGLE = 270

# Load and scale the images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png')
)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), Y_ANGLE
)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png')
)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), R_ANGLE
)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT)
)


# Function for drawing in the pygame window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    # Put a border in the middle
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        'Health remaining: ' + str(red_health), 1, WHITE
    )
    yellow_health_text = HEALTH_FONT.render(
        'Health remaining: ' + str(yellow_health), 1, WHITE
    )
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Bonus health
   # if random.randint(0, 100) == 37:
    #    for _ in range(200000):
      #      pygame.draw.rect(WIN, BLACK, BONUS_YELLOW)
    #if random.randint(0, 100) == 45:
     #   pygame.draw.rect(WIN, WHITE, BONUS_RED)


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Update the display
    pygame.display.update()


# Function for yellow spaceship movement
def yellow_movement(keys_pressed, yellow, Y_ANGLE=Y_ANGLE):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width: # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height - 10: #Down
        yellow.y += VEL
    if keys_pressed[pygame.K_e]: # Plan for rotating 
        pass

    

# Function for red spaceship movement
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 10: #Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH  - red.width: #Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height - 10: #Down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    # If bullets collide
    for yb in yellow_bullets:
        for rb in red_bullets:
            if yb.colliderect(rb):
                yellow_bullets.remove(yb)
                red_bullets.remove(rb)

        


# Function for declaring the winner on the screen
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    # Wait for 5 seconds and restart the game
    pygame.time.delay(3000)
    

# Main function
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5
                    )
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5
                    )
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_health -= 0.5
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 0.5
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = 'Yellow wins'
        if yellow_health <= 0:
            winner_text = 'Red wins'
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # If the loop breaks, restart the game
    main()


if __name__ == "__main__":
    main()
