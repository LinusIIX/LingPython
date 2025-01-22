import pygame
import random

pygame.init()

# Constants
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 600
FPS = 60
BIG_BAR_WIDTH = 20
BIG_BAR_HEIGHT = WINDOW_HEIGHT
PLAYER_BAR_WIDTH = 20
PLAYER_BAR_HEIGHT = 80
POINT_RADIUS = 10

PLAYER_SPEED = 3.5                  # Speed of the player bar movement per frame
POINT_TIME = 2                      # Seconds needed to score a point
POINT_SPEED = 2.5                   # Speed of the point movement per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (125,0,0)
GREEN = (0, 255, 0)
BLUE = (107, 204, 255)
BROWN = (125,80,30)
GREY = (75,75,75)

COLOR_ANGEL = BROWN
COLOR_FISH = RED
COLOR_WATER = BLUE
COLOR_BACK = WHITE

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mini Game")

# Clock
clock = pygame.time.Clock()

# Player bar initial position
player_x = (WINDOW_WIDTH - PLAYER_BAR_WIDTH) // 2 + 20
player_y = (WINDOW_HEIGHT - PLAYER_BAR_HEIGHT) // 2 + 20

# Point initial position and direction
point_y = random.randint(POINT_RADIUS, WINDOW_HEIGHT - POINT_RADIUS)
point_direction = random.choice([-1, 1])

# Timer for scoring
on_point_time = 0
score = 0

# Game loop
running = True
while running:
    screen.fill(COLOR_BACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - PLAYER_BAR_HEIGHT:
        player_y += PLAYER_SPEED

    # Draw big bar
    big_bar_x = (WINDOW_WIDTH - BIG_BAR_WIDTH) // 2 + 20
    pygame.draw.rect(screen, COLOR_WATER, (big_bar_x, 0, BIG_BAR_WIDTH, BIG_BAR_HEIGHT))

    # Draw player bar
    pygame.draw.rect(screen, COLOR_ANGEL, (player_x, player_y, PLAYER_BAR_WIDTH, PLAYER_BAR_HEIGHT))

    # Draw point
    point_x = big_bar_x + BIG_BAR_WIDTH // 2
    pygame.draw.circle(screen, COLOR_FISH, (point_x, point_y), POINT_RADIUS)

    # Move the point 
    point_y += POINT_SPEED * point_direction
    if point_y <= POINT_RADIUS +5 or point_y >= WINDOW_HEIGHT - POINT_RADIUS-5:
        # Reverse direction when hitting edges
        point_direction *= -1  

    # Randomly change direction with x% probability
    if random.random() < 0.02:
        point_direction *= -1

    # Check if player bar is on the point
    if player_y < point_y < player_y + PLAYER_BAR_HEIGHT:
        on_point_time += 1 / FPS
    else:
        on_point_time = 0

    # Check if the player has stayed on the point long enough to score
    # If so, increase the score and reset the timer
    if on_point_time >= POINT_TIME:
        score += 1
        on_point_time = 0
         
    # Draw score
    font = pygame.font.SysFont(None, 24)
    img = font.render(f'Score: {score}', True, GREY)
    screen.blit(img, (20, 20))

    # Draw on_point_time
    font = pygame.font.SysFont(None, 24)
    img = font.render(f'Time: {on_point_time:.2f}', True, GREY)
    screen.blit(img, (20, 40))


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
