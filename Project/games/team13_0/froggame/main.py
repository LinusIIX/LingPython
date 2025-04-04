import pygame
import random
import os

from assets import GameDataLink

#Written by Daniel
gameData = GameDataLink.get_data()
gameData["neededPoints"] = 1

pygame.init()



WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

Punkte = 0

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
background_path = os.path.join(BASE_DIR, "pond_background.png") 
background_img = pygame.image.load(background_path).convert()

background_img = pygame.transform.scale(background_img, (600, 600))


pygame.display.set_caption("Mini Game")

clock = pygame.time.Clock()

buttons = [
    pygame.Rect(200, 200, 40, 40),
    pygame.Rect(375, 190, 40, 40),
    pygame.Rect(275, 300, 40, 40),
    pygame.Rect(200, 400, 40, 40),
    pygame.Rect(375, 375, 40, 40),
]
time_giver = 1
clock = pygame.time.Clock()
timer_duration = time_giver
timer_start_ticks = pygame.time.get_ticks()

frosch_position = random.randint(1, 5)

frosch_health = 5
max_health = 5
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If the user clicks the close button before he caught the frog
            gameData["earnedPoints"] = 0
            GameDataLink.send_data(gameData)
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    if i + 1 == frosch_position:
                        Punkte += 1
                        frosch_health = frosch_health - 1
                        timer_duration = time_giver
                        random_number = random.randint(1, 5)
                        while random_number == frosch_position:
                            random_number = random.randint(1, 5)
                        frosch_position = random_number
                        timer_start_ticks = pygame.time.get_ticks() 


    screen.blit(background_img, (0, 0))

    for i, button in enumerate(buttons):
        if i + 1 == frosch_position:
            pygame.draw.rect(screen, (139, 69, 19), button)  # Braun
        else:
            pygame.draw.rect(screen, GREEN, button)

    seconds = (pygame.time.get_ticks() - timer_start_ticks) / 1000
    remaining_time = timer_duration - seconds
    if remaining_time <= 0:
        #print("Timer abgelaufen!")
        timer_duration = time_giver
        random_number = random.randint(1, 5)
        while random_number == frosch_position:
            random_number = random.randint(1, 5)
        frosch_position = random_number
        timer_start_ticks = pygame.time.get_ticks()  # Reset timer

    points_text = font.render(f"Punkte: {Punkte}", True, WHITE)
    screen.blit(points_text, (WINDOW_WIDTH - points_text.get_width() - 10, 10))

    # Draw the health bar
    health_bar_width = 200
    health_bar_height = 20
    health_ratio = frosch_health / max_health
    pygame.draw.rect(screen, RED, (10, 10, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, GREEN, (10, 10, health_bar_width * health_ratio, health_bar_height))

    if frosch_health <= 0: # If the frog is caught
        #print("Frosch gefangen!")
        gameData["rewardText"] = "Well done game finished, frog caught!"
        gameData["earnedPoints"] += 1
        GameDataLink.send_data(gameData)
        exit()

    


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
