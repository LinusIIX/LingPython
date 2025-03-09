# Author: 01/1455313	 Sahel kheireh
#         01/1480180	 Shunyu Xu
#         01/1479317	 Anqi Yuan
#         01/1367311	 Sahar Shahjalaledin
# Operating System: Windows 11
# Python Version: 3.13
# Required Libraries: Pygame

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
QUIZ_BG = (200, 200, 255)
INSTRUCTIONS_BG = (255, 228, 196)  # New color for the instructions page

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dothraki Language Quiz")
clock = pygame.time.Clock()

# Load Khal Drogo character image and set its initial position and speed
khal_drogo_img = pygame.image.load("assets/khal_drogo.png")
khal_drogo_img = pygame.transform.scale(khal_drogo_img, (40, 40))
khal_drogo_x, khal_drogo_y = WIDTH // 2 - 20, HEIGHT - 50
khal_drogo_speed = 8

# Load question mark image and resize it
question_mark_img = pygame.image.load("assets/questionmark.png")
question_mark_img = pygame.transform.scale(question_mark_img, (50, 50))

# Load tick mark image and resize it
tick_img = pygame.image.load("assets/tick.png")
tick_img = pygame.transform.scale(tick_img, (50, 50))

# Track completion status of quizzes
completed_quizzes = [False] * 7

# Define quiz zones where the quizzes will be triggered
quiz_zones = [
    pygame.Rect(120, 100, 50, 50),
    pygame.Rect(500, 150, 50, 50),
    pygame.Rect(80, 350, 50, 50),
    pygame.Rect(430, 400, 50, 50),
    pygame.Rect(250, 220, 50, 50),
    pygame.Rect(680, 200, 50, 50),
    pygame.Rect(450, 50, 50, 50)
]

# Variables for managing the current quiz state
current_quiz = -1
quiz_active = False
show_interact_text = False

# Movement variables to track Khal Drogo's movement direction
moving_right = False
moving_left = False
moving_up = False
moving_down = False

# Define collectibles and their initial states
collectibles = [
    pygame.Rect(180, 150, 30, 30),
    pygame.Rect(480, 200, 30, 30),
    pygame.Rect(100, 400, 30, 30),
    pygame.Rect(700, 450, 30, 30),
    pygame.Rect(350, 370, 30, 30),
    pygame.Rect(150, 500, 30, 30),
    pygame.Rect(600, 50, 30, 30),
    pygame.Rect(400, 300, 30, 30),
    pygame.Rect(300, 100, 30, 30),
    pygame.Rect(500, 400, 30, 30)
]
collected = [False] * 10
gold_counter = 0

# Define the quiz questions and correct answers with translations
questions = [
    {"type": "word_order", "words": ["dothrae","Anha", "she",  "rhaeshisar"], "correct": ["Anha", "dothrae", "rhaeshisar", "she"], "translation": ["ride","I",  "on", "the land"], "clue": "Clue: rhaeshisar (land) comes before she (on)."},
    {"type": "word_order", "words": ["she", "vekhat", "haji", "Rhaggat"], "correct": ["Rhaggat", "vekhat", "haji", "she"], "translation": [ "in", "stands", "the tent","dog"], "clue": "Clue: haji (tent) comes before she (in)."},
    {"type": "word_order", "words": ["vekhat","Rhaesh",  "hoshor", "vezhof"], "correct": ["Rhaesh", "vekhat", "vezhof", "hoshor"], "translation": ["stands","warrior",   "in front of","the horse"], "clue": "Clue: vezhof (horse) comes before hoshor (in front of)."},
    {"type": "multiple_choice", "question": "Vezhof vekhat ________.", "choices": ["azho she", "she azho"], "correct": "azho she", "translation": ["The horse is standing on the field."], "clue": "Clue: azho (field) comes before she (on)."},
    {"type": "multiple_choice", "question": "Anha vekhat ________.", "choices": ["kash hoshor", "hoshor kash"], "correct": "kash hoshor", "translation": ["I stand before the king."], "clue": "Clue: kash (king) comes before hoshor (before)."},
    {"type": "multiple_choice", "question": "Khaleesi vekhat vemish _____ .", "choices": ["she", "hoshor"], "correct": "she", "translation": ["The queen walks on the road."], "clue": ""},
    {"type": "multiple_choice", "question": "Haji vekhat vezhof ________.", "choices": ["she", "hoshor"], "correct": "hoshor", "translation": ["The dog stands in front of the horse."], "clue": ""}
]

# Variables to track selected words during the quiz
selected_words = []
word_slots = []

# Game state variable
game_state = "instructions"

# Function to draw text on the screen
def draw_text(text, x, y, color=BLACK, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw the game elements on the screen
def draw_game():
    screen.fill(GREEN)  # Filling the screen with green color
    draw_trees()  # Drawing trees in the background
    screen.blit(khal_drogo_img, (khal_drogo_x, khal_drogo_y))  # Drawing Khal Drogo character
    # Drawing quiz locations with question marks and tick marks for completed quizzes
    for i, zone in enumerate(quiz_zones):
        screen.blit(question_mark_img, (zone.x, zone.y))
        if completed_quizzes[i]:
            screen.blit(tick_img, (zone.x, zone.y))
    # Drawing collectibles
    for i, col in enumerate(collectibles):
        if not collected[i]:
            pygame.draw.rect(screen, YELLOW, col)
    # Drawing the gold counter
    draw_text(f"Gold: {gold_counter}", WIDTH - 150, 10, BLACK, 36)
    # Showing interaction text if near a quiz zone
    if show_interact_text:
        draw_text("Press E to start the quiz", WIDTH // 2 - 150, HEIGHT - 50, BLACK, 30)
    # Drawing the quiz interface if a quiz is active
    if quiz_active:
        draw_quiz()
    pygame.display.flip()  # Updating the display

# Function to draw trees on the screen
def draw_trees():
    # Fixed positions for trees
    tree_positions = [
        (100, 100), (200, 300), (300, 500), (500, 250), (700, 150),
        (150, 200), (300, 350), (450, 150), (600, 450), (750, 350)
    ]
    # Drawing trees if they don't overlap with quiz zones
    for pos in tree_positions:
        tree_rect = pygame.Rect(pos[0], pos[1], 50, 50)
        if not any(tree_rect.colliderect(zone) for zone in quiz_zones):
            pygame.draw.circle(screen, DARK_GREEN, pos, 20)

# Function to draw the quiz interface
def draw_quiz():
    screen.fill(QUIZ_BG)  # Setting background color for the quiz
    if questions[current_quiz]["type"] == "word_order":
        words = questions[current_quiz]["words"]
        translations = questions[current_quiz]["translation"]
        clue = questions[current_quiz]["clue"]
        global word_slots
        word_slots = []
        # Calculating starting positions for words
        start_x = (WIDTH - len(words) * 100) // 2
        start_y = HEIGHT // 3
        # Drawing word slots
        for idx, word in enumerate(words):
            word_rect = pygame.Rect(start_x + idx * 100, start_y, 90, 50)
            pygame.draw.rect(screen, BLACK, word_rect, 2)
            draw_text(word, word_rect.x + 5, word_rect.y + 10, BLUE, 28)
            draw_text(translations[idx], word_rect.x + 5, word_rect.y + 60, BLACK, 20)
            word_slots.append((word, word_rect))

        # Drawing selection slots
        slot_y = HEIGHT // 2
        for i in range(len(words)):
            slot = pygame.Rect(start_x + i * 100, slot_y, 90, 50)
            pygame.draw.rect(screen, BLACK, slot, 2)
            if i < len(selected_words):
                draw_text(selected_words[i], slot.x + 5, slot.y + 10, BLACK, 28)

        # Adding instruction text for deleting selected words and buying clues
        draw_text("Touch a word again to remove it from selection.", WIDTH // 2 - 200, slot_y + 100, BLACK, 24)
        draw_text("Press C to buy a clue for 2 gold.", WIDTH // 2 - 150, slot_y + 130, BLACK, 24)
        # Drawing the clue if available
        if clue:
            draw_text(clue, WIDTH // 2 - 200, slot_y + 160, BLACK, 24)
    else:
        question = questions[current_quiz]["question"]
        choices = questions[current_quiz]["choices"]
        translations = questions[current_quiz]["translation"]
        clue = questions[current_quiz]["clue"]
        
        # Drawing translations above the question for all multiple-choice questions
        draw_text(translations[0], WIDTH // 2 - 200, HEIGHT // 3 - 50, BLACK, 20)
        
        draw_text(question, WIDTH // 2 - 200, HEIGHT // 3, BLACK, 28)
        for idx, choice in enumerate(choices):
            draw_text(f"{idx + 1}. {choice}", WIDTH // 2 - 200, HEIGHT // 3 + (idx + 1) * 40, BLACK, 28)
        draw_text("Press 1 or 2 to choose the correct answer.", WIDTH // 2 - 200, HEIGHT // 3 + 3 * 40, BLACK, 24)
        # Drawing the clue if available
        if clue:
            draw_text(clue, WIDTH // 2 - 200, HEIGHT // 3 + 4 * 40, BLACK, 24)

    # Drawing the gold counter in the quiz page
    draw_text(f"Gold: {gold_counter}", WIDTH - 150, 10, BLACK, 36)
    
    pygame.display.flip()  # Updating the display

# Function to draw the instruction screen
def draw_instructions():
    screen.fill(INSTRUCTIONS_BG)  # Setting background color for the instructions page
    draw_text("Welcome to Dothraki Language Quiz!", WIDTH // 2 - 250, HEIGHT // 4 - 60, BLACK, 48)
    pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 170, 600, 320), 2)
    draw_text("Instructions:", WIDTH // 2 - 100, HEIGHT // 2 - 150, BLACK, 36)
    draw_text("1. Move with arrow keys", WIDTH // 2 - 290, HEIGHT // 2 - 110, BLACK, 28)
    draw_text("2. Collect gold to buy clues", WIDTH // 2 - 290, HEIGHT // 2 - 80, BLACK, 28)
    draw_text("3. Reach quiz zones and press 'E' to start", WIDTH // 2 - 290, HEIGHT // 2 - 50, BLACK, 28)
    draw_text("4. Arrange words in the correct order", WIDTH // 2 - 290, HEIGHT // 2 - 20, BLACK, 28)
    draw_text("5. Press 'C' to buy a clue for 2 gold", WIDTH // 2 - 290, HEIGHT // 2 + 10, BLACK, 28)
    draw_text("Purpose: Teach basic grammar rules and words", WIDTH // 2 - 290, HEIGHT // 2 + 50, BLACK, 28)
    draw_text("Word order: Subject (S) Verb (V) Object (O)", WIDTH // 2 - 290, HEIGHT // 2 + 80, BLACK, 28)
    draw_text("Press 'Enter' to start the game", WIDTH // 2 - 150, HEIGHT // 2 + 150, BLACK, 36)
    pygame.display.flip()

# Function to check if the selected words match the correct answer
def check_answer():
    if questions[current_quiz]["type"] == "word_order":
        return len(selected_words) == len(questions[current_quiz]["correct"]) and selected_words == questions[current_quiz]["correct"]
    else:
        return selected_words[0] == questions[current_quiz]["correct"]

# Function to display congratulations message
def show_congrats():
    for _ in range(3):
        screen.fill(QUIZ_BG)
        draw_text("Congratulations!", WIDTH // 2 - 90, HEIGHT // 4, BLACK, 48)
        pygame.display.flip()
        pygame.time.delay(500)
        screen.fill(QUIZ_BG)
        pygame.display.flip()
        pygame.time.delay(500)

# Function to display try again message
def show_try_again():
    draw_text("Try Again!", WIDTH // 2 - 70, HEIGHT // 4, BLACK, 48)
    pygame.display.flip()
    pygame.time.delay(1000)

# Function to check if all quizzes are completed
def check_game_over():
    return all(completed_quizzes)

# Function to display game over message
def show_game_over():
    screen.fill(QUIZ_BG)
    draw_text("Good Job!", WIDTH // 2 - 70, HEIGHT // 2 - 100, BLACK, 48)
    draw_text(f"Gold: {gold_counter}", WIDTH // 2 - 70, HEIGHT // 2 - 24, BLACK, 48)
    draw_text("Prepositions come after the object.", WIDTH // 2 - 300, HEIGHT // 2 + 70, BLACK, 28)
    draw_text("Vezhof = Horse", WIDTH // 2 - 300, HEIGHT // 2 + 100, BLACK, 28)
    draw_text("Vekhat = Stands", WIDTH // 2 - 300, HEIGHT // 2 + 130, BLACK, 28)
    draw_text("Haji = Dog", WIDTH // 2 - 300, HEIGHT // 2 + 160, BLACK, 28)
    draw_text("Hoshor = In front of", WIDTH // 2 - 300, HEIGHT // 2 + 190, BLACK, 28)
    draw_text("rhaeshisar = the land", WIDTH // 2-300, HEIGHT // 2 + 220, BLACK, 28)
    draw_text("She = on", WIDTH // 2, HEIGHT // 2 + 100, BLACK, 28)
    draw_text("kash = king", WIDTH // 2, HEIGHT // 2 + 130, BLACK, 28)
    draw_text("Anha = I", WIDTH // 2, HEIGHT // 2 + 160, BLACK, 28)
    draw_text("azho = field", WIDTH // 2, HEIGHT // 2 + 190, BLACK, 28)
    draw_text("Rhaesh = warrior", WIDTH // 2, HEIGHT // 2 + 220, BLACK, 28)
    draw_text("dothrae = ride", WIDTH // 2, HEIGHT // 2 + 250, BLACK, 28)
    
    draw_text("Press 'Esc' to exit the game", WIDTH // 2 - 100, HEIGHT // 2 + 270, BLACK, 36)
    pygame.display.flip()
    waiting_for_exit = True
    while waiting_for_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

# Function to provide a clue
def provide_clue():
    global gold_counter
    if (gold_counter >= 2) and (len(selected_words) < len(questions[current_quiz]["correct"])):
        gold_counter -= 2
        for i, word in enumerate(questions[current_quiz]["correct"]):
            if i >= len(selected_words) or selected_words[i] != word:
                selected_words.insert(i, word)
                break

# Main game loop
running = True
while running:
    screen.fill(GREEN)  # Filling the screen with green color

    if game_state == "instructions":
        draw_instructions()
    else:
        draw_game()  # Drawing game elements

    show_interact_text = False
    for i, zone in enumerate(quiz_zones):
        if zone.colliderect(pygame.Rect(khal_drogo_x, khal_drogo_y, 40, 40)):
            show_interact_text = True
            break

     # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checking for window close event
            running = False
        elif event.type == pygame.KEYDOWN:  # Checking for key press events
            if game_state == "instructions":
                if event.key == pygame.K_RETURN:
                    game_state = "game"
            else:
                if event.key == pygame.K_RIGHT:  # Moving right
                    moving_right = True
                elif event.key == pygame.K_LEFT:  # Moving left
                    moving_left = True
                elif event.key == pygame.K_UP:  # Moving up
                    moving_up = True
                elif event.key == pygame.K_DOWN:  # Moving down
                    moving_down = True
                elif event.key == pygame.K_e and not quiz_active:  # Starting quiz if 'E' is pressed and no quiz is active
                    for i, zone in enumerate(quiz_zones):
                        # Checking if Khal Drogo is in a quiz zone and the quiz is not completed
                        if zone.colliderect(pygame.Rect(khal_drogo_x, khal_drogo_y, 40, 40)) and not completed_quizzes[i]:
                            quiz_active = True
                            current_quiz = i
                            selected_words = []
                elif event.key == pygame.K_c and quiz_active:  # Buying a clue
                    provide_clue()
                elif event.key == pygame.K_1 or event.key == pygame.K_2:
                    if quiz_active and questions[current_quiz]["type"] == "multiple_choice":
                        selected_words = [questions[current_quiz]["choices"][event.key - pygame.K_1]]
                        if check_answer():
                            completed_quizzes[current_quiz] = True
                            show_congrats()  # Showing congratulations message
                            quiz_active = False
                        else:
                            show_try_again()
                            selected_words = []
        elif event.type == pygame.KEYUP:  # Checking for key release events
            if event.key == pygame.K_RIGHT:  # Stopping moving right
                moving_right = False
            if event.key == pygame.K_LEFT:  # Stopping moving left
                moving_left = False
            if event.key == pygame.K_UP:  # Stopping moving up
                moving_up = False
            if event.key == pygame.K_DOWN:  # Stopping moving down
                moving_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN and quiz_active:  # Checking for mouse button press during a quiz
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for word, rect in word_slots:
                # Checking if a word slot is clicked
                if rect.collidepoint(mouse_x, mouse_y):
                    if word in selected_words:  # Removing word if already selected
                        selected_words.remove(word)
                    elif len(selected_words) < len(questions[current_quiz]["correct"]):  # Adding word if not selected
                        selected_words.append(word)
            draw_quiz()
            if check_answer():  # Checking if the answer is correct
                completed_quizzes[current_quiz] = True
                show_congrats()  # Showing congratulations message
                quiz_active = False
            elif len(selected_words) == len(questions[current_quiz]["correct"]):  # Showing try again message if wrong
                show_try_again()
                selected_words = []

    # Checking for collectible collisions
    for i, col in enumerate(collectibles):
        if col.colliderect(pygame.Rect(khal_drogo_x, khal_drogo_y, 40, 40)) and not collected[i]:
            collected[i] = True
            gold_counter += 1

    # Moving Khal Drogo based on the movement flags
    if moving_right:
        # Calculate the new x-coordinate by adding the speed to the current x-coordinate
        new_x = khal_drogo_x + khal_drogo_speed
        # Check if the new x-coordinate plus the width of the image is within the screen width
        if new_x + khal_drogo_img.get_width() <= WIDTH:
            # Update the x-coordinate of Khal Drogo's position
            khal_drogo_x = new_x
    if moving_left:
        # Calculate the new x-coordinate by subtracting the speed from the current x-coordinate
        new_x = khal_drogo_x - khal_drogo_speed
        # Check if the new x-coordinate is greater than or equal to 0 (left screen boundary)
        if new_x >= 0:
            # Update the x-coordinate of Khal Drogo's position
            khal_drogo_x = new_x
    if moving_up:
        # Calculate the new y-coordinate by subtracting the speed from the current y-coordinate
        new_y = khal_drogo_y - khal_drogo_speed
        # Check if the new y-coordinate is greater than or equal to 0 (top screen boundary)
        if new_y >= 0:
            # Update the y-coordinate of Khal Drogo's position
            khal_drogo_y = new_y
    if moving_down:
        # Calculate the new y-coordinate by adding the speed to the current y-coordinate
        new_y = khal_drogo_y + khal_drogo_speed
        # Check if the new y-coordinate plus the height of the image is within the screen height
        if new_y + khal_drogo_img.get_height() <= HEIGHT:
            # Update the y-coordinate of Khal Drogo's position
            khal_drogo_y = new_y

    # Checking if the game is over
    if check_game_over():
        show_game_over()

    # Controlling the frame rate
    clock.tick(30)

# Quitting Pygame
pygame.quit()