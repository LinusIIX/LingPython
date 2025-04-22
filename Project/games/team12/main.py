import sys
import os
import pygame
from pygame.locals import *
import random
import time
from assets import GameDataLink  # Ensures integration with Game Engine Interface

# ========== AUTHORS ==========
# - Durasin David, Izairi Alban
# - Code ran on Windows 11 (David) & Windows 10 (Alban) with Python 3.12.9
# - David: Wrote the game logic and mechanics
# - Alban: Integrated it into the full project and made modifications
# - https://www.pexels.com/photo/trees-on-a-dark-forest-1671325/ - background picture link
# - This code is a Pygame-built Dothraki imperative word translation quiz in which 
# - players have ten seconds to choose the appropriate English translation for a given 
# - Dothraki word. When the player gets 10 right answers, it shows a "Congratulations" 
# - screen, while it records the player's score and gives immediate feedback. At the end 
# - of the game, you can either restart or quit.
# ==================================

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Imperative Mood Challenge")

# Load background image
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the script's directory
background_path = os.path.join(BASE_DIR, "background.png") # Path to background image

# Make sure the background image exists
if not os.path.exists(background_path):
    print(f"ERROR: Background image not found at {background_path}")
    exit()

background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255) # Standard white text
BLACK = (0, 0, 0) # Button borders
GREEN = (0, 255, 0) # Correct answer highlight
RED = (255, 0, 0) # Wrong answer highlight

# Set up fonts
font = pygame.font.Font(None, 36) # Default font with size 36

# Retrieve game data
gameData = GameDataLink.get_data()
gameData["neededPoints"] = 10 # Number of correct answers needed to win
gameData["text"] = "Translate the Dothraki imperative words!"
gameData["earnedPoints"] = 0  # Ensure earnedPoints starts at 0

# List of imperative words (Dothraki -> English Imperative)
words = [
    ("Adakhat!", "Eat!"),
    ("Anat!", "Jog!"),
    ("Assilat!", "Signal!"),
    ("Charolat!", "Listen!"),
    ("Chilat!", "Lie down!"),
    ("Chomat!", "Respect!"),
    ("Chetirat!", "Canter!"),
    ("Ezzolat!", "Teach!"),
    ("Evolat!", "Start!"),
    ("Evvat!", "Begin!"),
    ("Eyelat!", "Move!"),
    ("Fonat!", "Hunt!"),
    ("Fonolat!", "Track!"),
    ("Frakhat!", "Touch!"),
    ("Fredrilat!", "Run!"),
    ("Gachat!", "Solve!"),
    ("Garvolat!", "Grow hungry!"),
    ("Gendolat!", "Ripped!"),
    ("Hoyalat!", "Sing!"),
    ("Iddelat!", "Welcome!"),
    ("Indelat!", "Drink!"),
    ("Irvosat!", "Trot!"),
    ("Ittelat!", "Improve!"),
    ("Jasat!", "Laugh!"),
    ("Lekhilat!", "Taste!"),
    ("Kashat!", "Last!"),
    ("Qafat!", "Ask!"),
    ("Shilat!", "Know!"),
    ("Zorat!", "Roar!")
]
random.shuffle(words)  # Shuffle words so each game is different


# Function to get 3 incorrect options along with the correct one
def get_options(correct_translation):
    """Generates three incorrect options and one correct answer."""
    incorrect_choices = random.sample([w[1] for w in words if w[1] != correct_translation], 3)
    return incorrect_choices + [correct_translation]

# Initialize game variables
current_word, correct_translation = words.pop()
options = get_options(correct_translation)
random.shuffle(options) # Randomize answer positions
start_time = time.time()
TIME_LIMIT = 10 # 10 seconds per question
waiting_for_next = False # Helps control when we move to the next question
message = "" # Stores feedback for the player
game_over = False  # **Tracks if the player won**

buttons = [] # Stores button objects
clock = pygame.time.Clock() # Controls frame rate

# ========== GAME LOOP ==========
running = True
while running:
    screen.blit(background, (0, 0)) # Draw background
    elapsed_time = time.time() - start_time # Get elapsed time
    remaining_time = max(0, TIME_LIMIT - int(elapsed_time)) # Prevents negative timer

    if game_over:
        # **Congratulations Screen**
        congrats_text = font.render("Congratulations! You won!", True, GREEN)
        screen.blit(congrats_text, (WIDTH // 2 - 150, 250))
        
        # Create "Restart" button
        restart_btn_rect = pygame.Rect(WIDTH // 2 - 120, 320, 240, 50)
        pygame.draw.rect(screen, BLACK, restart_btn_rect, 2)
        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - 50, 335))
        
        # Create "Quit" button
        quit_btn_rect = pygame.Rect(WIDTH // 2 - 120, 400, 240, 50)
        pygame.draw.rect(screen, BLACK, quit_btn_rect, 2)
        quit_text = font.render("Quit", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - 50, 415))

    elif not waiting_for_next:
        # Display the question
        question_text = font.render(f"What does '{current_word}' mean?", True, WHITE)
        screen.blit(question_text, (WIDTH // 2 - 150, 100))

        # Display player's score
        score_text = font.render(f"Score: {gameData['earnedPoints']}/{gameData['neededPoints']}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 50, 50))  # Position near the top

        # Display timer
        timer_text = font.render(f"Time left: {remaining_time}s", True, RED if remaining_time <= 3 else WHITE)
        screen.blit(timer_text, (WIDTH // 2 - 50, 150))


        # Update buttons
        buttons = []
        for i, option in enumerate(options):
            btn_rect = pygame.Rect(WIDTH // 2 - 120, 200 + i * 60, 240, 50)
            buttons.append((btn_rect, option))
            pygame.draw.rect(screen, BLACK, btn_rect, 2)
            option_text = font.render(option, True, WHITE)
            screen.blit(option_text, (WIDTH // 2 - 110, 210 + i * 60))
    else:
        # Display "Correct!" message and Next Question button
        message_text = font.render("Correct!", True, GREEN)
        screen.blit(message_text, (WIDTH // 2 - 50, 300))

        next_btn_rect = pygame.Rect(WIDTH // 2 - 120, 350, 240, 50)
        pygame.draw.rect(screen, BLACK, next_btn_rect, 2)
        next_text = font.render("Next Question", True, WHITE)
        screen.blit(next_text, (WIDTH // 2 - 100, 365))

    # Display feedback message
    message_text = font.render(message, True, RED)
    screen.blit(message_text, (WIDTH // 2 - 50, 450))

    pygame.display.flip() # Refresh screen

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                # **Handle clicks on Congratulations screen**
                if restart_btn_rect.collidepoint(event.pos):
                    gameData["earnedPoints"] = 0  # Reset score
                    words = random.sample(words, len(words))  # Shuffle words again
                    current_word, correct_translation = words.pop()
                    options = get_options(correct_translation)
                    random.shuffle(options)
                    start_time = time.time()
                    message = ""
                    waiting_for_next = False
                    game_over = False  # Restart game
                elif quit_btn_rect.collidepoint(event.pos):
                    running = False  # Exit game
            elif waiting_for_next:
                if next_btn_rect.collidepoint(event.pos):
                    if words:
                        current_word, correct_translation = words.pop()
                        options = get_options(correct_translation)
                        random.shuffle(options)
                        start_time = time.time()
                        message = ""
                        waiting_for_next = False
                    else:
                        game_over = True  # **Player has answered all questions**
            else:
                for btn_rect, option in buttons:
                    if btn_rect.collidepoint(event.pos):
                        if option == correct_translation:
                            pygame.draw.rect(screen, GREEN, btn_rect, 2)
                            pygame.display.flip()
                            pygame.time.delay(500)
                            gameData["earnedPoints"] += 1
                            if gameData["earnedPoints"] >= gameData["neededPoints"]:
                                game_over = True  # **Trigger Congratulations screen**
                            else:
                                waiting_for_next = True
                        else:
                            pygame.draw.rect(screen, RED, btn_rect, 2)
                            pygame.display.flip()
                            pygame.time.delay(500)
                            message = "Try again!"

    # Check for timeout
    if remaining_time == 0 and not waiting_for_next and not game_over:
        message = "Time's up!"
        pygame.time.delay(1000)
        if words:
            current_word, correct_translation = words.pop()
            options = get_options(correct_translation)
            random.shuffle(options)
            start_time = time.time()
            message = ""
        else:
            game_over = True  # **No more words, show Congratulations screen**

    clock.tick(30)

pygame.quit()
