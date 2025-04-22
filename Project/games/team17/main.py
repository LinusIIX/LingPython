import pygame
from pygame.locals import *
from assets import GameDataLink
import random

#Creator: Mark Cule
#Python 3.12.3
#Distributor ID:	Ubuntu
#Description:	Ubuntu 24.04.1 LTS
#Release:	24.04
#Codename:	noble


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 980
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
RULES = """
    Welcome to the Dothraki noun learning Game!\n
    * Game mechanics:\n
        - Choose the amount of nouns to be used\n
        - Over time nouns will be shown\n
        - You have to remember which nouns have been shown\n
        - If a english noun is shown then your response should\n 
          adhere to the following grammar as denoted by this regex:\n
            - (1|2)" "( |translation into dorthraki)\n
        - 1 denotes that the dothraki equivalent noun has been shown\n 
          already and 2 that it has not\n
        - You get points for each correct guess and extra points for\n 
          the translation into dorthraki\n
        - An incorrect guess ends the game.\n
    - The game is won when all Dothraki nouns and their translations\n
      have been displayed atleast once.\n
    - When modifiying the dictionary make sure to enter like this:\n
        - "Dothraki_noun English_translation" so that its seperated\n
           by space
    """
#Each state distinctly handles drawing and events
MAIN_MENU_STATE = 1
DISPLAY_RULES_STATE = 2
DICTIONARY_STATE = 3
DORTHRAKI_NOUN_STATE = 4
AWAITING_NUM_OF_NOUNS_STATE = 5
TRANSLATION_STATE = 6
CORRECT_GUESS_STATE = 7
LOST_STATE = 8
WIN_STATE = 9

#Multiple rectangle/box presets 
POS_1_B = pygame.Rect(WIDTH//4, HEIGHT//3, 300, 80)
POS_2_B = pygame.Rect(WIDTH//4, HEIGHT//3 + 100, 300, 80)
POS_3_B = pygame.Rect(WIDTH//4, HEIGHT//3 + 200, 300, 80)
POS_4_B = pygame.Rect(WIDTH//20, HEIGHT//2 + 150, 300, 80)
POS_5_B = pygame.Rect(WIDTH - 350, 100, 250, 50)
POS_6_B = pygame.Rect(WIDTH - 350, 200, 250, 50)
POS_7_B = pygame.Rect(WIDTH - 350, HEIGHT - 150, 250, 50)
POS_8_B = pygame.Rect(WIDTH - 350, HEIGHT - 250, 250, 50)
POS_9_B = pygame.Rect(WIDTH//4, HEIGHT//3+400, 300, 50)
POS_10_B = pygame.Rect(WIDTH//4, HEIGHT//3+300, 300, 50)
POS_11_B = pygame.Rect(WIDTH//4, HEIGHT//3+360, 300, 50)


# Create the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dothraki Noun Learning Game")

def draw_text(text, x, y, color=BLACK):
    render = FONT.render(text, True, color)
    screen.blit(render, (x, y))

# Function to draw text and handle newlines
def draw_multiline_text(text, x, y, color=BLACK):
    lines = text.split('\n')  # Split the text into lines wherever there is a newline character
    y_offset = y
    for line in lines:
        draw_text(line, x, y_offset)
        y_offset += FONT.get_height()  # Add some space between lines
    
# Display function for the MAIN_MENU_STATE
def main_menu():
    screen.fill(WHITE)
    draw_text("Dothraki Noun Learning Game", WIDTH//4, HEIGHT//6)
    pygame.draw.rect(screen, BLACK, POS_1_B, 2)
    pygame.draw.rect(screen, BLACK, POS_2_B, 2)
    pygame.draw.rect(screen, BLACK, POS_3_B, 2)
   
    draw_text("Play", WIDTH//4 + 110, HEIGHT//3 + 15)
    draw_text("Rules", WIDTH//4 + 110, HEIGHT//3 + 115)
    draw_text("Dictionary", WIDTH//4 + 50, HEIGHT//3 + 215)
    return

def display_rules():
    screen.fill(WHITE)
    draw_multiline_text(RULES, WIDTH//4, HEIGHT//20)
    pygame.draw.rect(screen, BLACK, POS_4_B, 2)
    draw_text("Go back", POS_4_B.x + 90, POS_4_B.y + 20)
    return

def display_text(text):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, POS_9_B, 2)
    draw_text("Next", POS_9_B.x + 100, POS_9_B.y + 10)
    draw_multiline_text(text, POS_9_B.x, POS_9_B.y - 300)
    return

def display_dictionary(dothraki_dict,text_input,writing):
    screen.fill(WHITE)
    
    # Draw dictionary key-value pairs
    y_offset = 60
    for key, value in dothraki_dict.items():
        draw_text(f"{key}: {value}", 50, y_offset)
        y_offset += FONT.get_height() + 10

    # Draw boxes
    pygame.draw.rect(screen, BLACK, POS_5_B, 2)
    pygame.draw.rect(screen, BLACK, POS_6_B, 2)
    pygame.draw.rect(screen, BLACK, POS_7_B, 2)
    
    draw_text("Add", POS_5_B.x + 100, POS_5_B.y + 10)
    draw_text("Remove", POS_6_B.x + 80, POS_6_B.y + 10)
    draw_text("Go Back", POS_7_B.x + 80, POS_7_B.y + 10)
    
    # Drawing the input box
    pygame.draw.rect(screen, BLACK, POS_8_B, 2)
    if writing:
        draw_text("Writing", POS_8_B.x + 10, POS_8_B.y-25)
    else: 
        draw_text("Write here", POS_8_B.x + 10, POS_8_B.y-25)
    draw_text(":" + text_input, POS_8_B.x + 10, POS_8_B.y + 10)
    return

def add_to_dictionary(text_input, dictionary):
    parts = text_input.split(" ", 1)  # Split at first space to get noun and translation
    if len(parts) == 2:
        dothraki_noun, english_translation = parts
        if dothraki_noun not in dictionary:  # Avoid duplicate entries
            dictionary[dothraki_noun] = english_translation
            print(f"Added: {dothraki_noun} -> {english_translation}")
        else:
            print(f"'{dothraki_noun}' already exists in the dictionary!")
    else:
        print("Invalid format! Use: Dothraki_noun English_translation")
    return dictionary

def remove_from_dictionary(text_input, dictionary):
    parts = text_input.split(" ", 1)  # Extract the Dothraki noun (ignore translation part)
    dothraki_noun = parts[0]  # We only need the first part to delete
    if dothraki_noun in dictionary:
        del dictionary[dothraki_noun]
        print(f"Removed: {dothraki_noun}")
    else:
        print(f"'{dothraki_noun}' not found in dictionary!")
    return dictionary

def display_noun_count_prompt(text_input,writing):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, POS_9_B, 2)
    draw_text("Next", POS_9_B.x + 100, POS_9_B.y + 10)
    
    # Drawing the input box
    pygame.draw.rect(screen, BLACK, POS_10_B, 2)
    if writing:
        draw_text("Writing", POS_10_B.x + 10, POS_10_B.y-25)
    else: 
        draw_text("Write here", POS_10_B.x + 10, POS_10_B.y-25)
    draw_text(":" + text_input, POS_10_B.x + 10, POS_10_B.y + 10)
    draw_text("Enter the amount of Dorthraki-English translation pairs to be used in the game",WIDTH//20, HEIGHT//2)
    return

def display_translation(translation,writing,text_input):
    screen.fill(WHITE)

    draw_text("Has this translation's Dothraki word been shown? (1 = Yes, 2 = No) --> " + translation, WIDTH//20,HEIGHT//5)
    pygame.draw.rect(screen, BLACK, POS_10_B, 2)
    if writing:
        draw_text("Writing", POS_10_B.x + 10, POS_10_B.y-25)
    else: 
        draw_text("Write here", POS_10_B.x + 10, POS_10_B.y-25)
    draw_text(":" + text_input, POS_10_B.x + 10, POS_10_B.y + 10)
    pygame.draw.rect(screen, BLACK, POS_11_B, 2)
    draw_text("Make guess",POS_11_B.x+40, POS_11_B.y+10)

def game_loop():
    gameData = GameDataLink.get_data()
    gameData["neededPoints"] = 50  # Set needed points
    gameData["text"] = "Dothraki noun learning game!"
    earned_points = gameData["earnedPoints"]

    running = True
    state = MAIN_MENU_STATE
    text = ""   # Helping variable to store text
    text_input = ""  # This will hold the text entered by the player
    writing = False
    num_nouns = 0
    noun = "" # Stores the dothraki noun to be displayed
    selected_word = "" # Stores the translation to be displayed (However it is stores the dorthraki noun)
    selected_words = [] # Randomly will take num_words many dorthraki words from dictionary
    used_dothraki = [] 
    unused_dothraki = []
    unused_translations = set()
    used_translations = set()  
    score = 0
    
    dothraki_dict = {
        "anha": "I", "yer": "you", "rakh": "warrior", "zhey": "hello", "athdrivar": "battle",
        "haji": "leave", "thirar": "see", "rhaesh": "land", "khaleesi": "queen", "vaz": "to go",
        "vezof": "gift", "dothraki": "rider", "chiftik": "insect", "oon": "for",
        "khaleen": "widow", "sajo": "helmet", "rhaeshisar": "kingdom", "torga": "tribe", "vikeesi": "friend"
    }

    while running:
        screen.fill(WHITE)
        if state == MAIN_MENU_STATE:
            main_menu()
        elif state == DISPLAY_RULES_STATE:
            display_rules()
        elif state == DICTIONARY_STATE:
            display_dictionary(dothraki_dict, text_input,writing)
        elif state == DORTHRAKI_NOUN_STATE:
            display_text(noun)
        elif state == AWAITING_NUM_OF_NOUNS_STATE:
            display_noun_count_prompt(text_input, writing)
        elif state == TRANSLATION_STATE:
            display_translation(dothraki_dict.get(selected_word),writing,text_input)
        elif state == WIN_STATE or LOST_STATE or CORRECT_GUESS_STATE:
            display_text(text)


        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                gameData["earnedPoints"] = earned_points
                GameDataLink.send_data(gameData)  # Save progress

            elif event.type == KEYDOWN and writing:
                if event.key == K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key != K_RETURN:
                    text_input += event.unicode

            elif state == MAIN_MENU_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_1_B.collidepoint(event.pos):
                        print("Play game")
                        state = AWAITING_NUM_OF_NOUNS_STATE

                    elif POS_2_B.collidepoint(event.pos):
                        print("Display rules")
                        state = DISPLAY_RULES_STATE

                    elif POS_3_B.collidepoint(event.pos):
                        print("Show dictionary")
                        state = DICTIONARY_STATE

            elif state == DISPLAY_RULES_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_4_B.collidepoint(event.pos):
                        state = MAIN_MENU_STATE
                        
            elif state == DICTIONARY_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_7_B.collidepoint(event.pos):
                        state = MAIN_MENU_STATE
                        text_input = ""

                    elif POS_8_B.collidepoint(event.pos):
                        writing = not writing

                    elif POS_5_B.collidepoint(event.pos):
                        dothraki_dict = add_to_dictionary(text_input, dothraki_dict)
                        text_input = ""

                    elif POS_6_B.collidepoint(event.pos):
                        dothraki_dict = remove_from_dictionary(text_input, dothraki_dict)
                        text_input = ""

            elif state == AWAITING_NUM_OF_NOUNS_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_9_B.collidepoint(event.pos):
                        if not text_input.isdigit():  # Check if input is a natural number \ 0
                            print("Error: Input must be a natural number (positive integer starting from 1).")        
                        else: 
                            #setup the game variables
                            num_nouns = int(text_input)
                            state = DORTHRAKI_NOUN_STATE
                            selected_words = random.sample(list(dothraki_dict.keys()), num_nouns)
                            unused_dothraki = selected_words[:]
                            unused_translations = set(selected_words)
                            writing = False
                            text_input = ""
                            random.shuffle(unused_dothraki)
                            noun = unused_dothraki.pop(0)
                            used_dothraki.append(noun)
                            score += num_nouns * 3

                    elif POS_10_B.collidepoint(event.pos):
                        writing = not writing

            elif state == DORTHRAKI_NOUN_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_9_B.collidepoint(event.pos):
                        choice = random.choices(["new", "translation"], [0.25, 0.75])[0] #25% new dorthraki noun else a translation is prompted
                        if choice == "new" and unused_dothraki:
                            noun = unused_dothraki.pop(0)
                            used_dothraki.append(noun)
                        else:
                            state = TRANSLATION_STATE
                            if used_translations and random.choice([True, False]) or not unused_translations: 
                                selected_word = random.choice(list(used_translations))  # Previously used translation
                            else:
                                selected_word = unused_translations.pop()  # New translation
                                used_translations.add(selected_word)

            elif state == TRANSLATION_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_11_B.collidepoint(event.pos):
                        parts = text_input.split() #Splits the guess into a list
                        if len(parts) == 1 and parts[0] in ["1", "2"]:
                            response = parts[0]
                            correct_translation = False
                        elif len(parts) == 2 and parts[0] in ["1", "2"]:
                            response = parts[0]
                            correct_translation = parts[1] == selected_word
                        else:
                            print("Invalid input. Please enter '1' or '2',optionaly provide the correct Dothraki word for extra points.")
                            text_input = "input invalid!"
                            continue #handle next event
                        if (response == "1" and selected_word in used_dothraki) or (response == "2" and not (selected_word in used_dothraki)):
                            score += 3
                            state = CORRECT_GUESS_STATE
                            if correct_translation:
                                score += 5
                                print("Maximally correct!")
                                text = "Correct guess with bonus!"
                            else:
                                print("Correct!")
                                text = "Correct guess with no bonus!"
                        else:
                            state = LOST_STATE
                            text = f"You lost and you had: {score} points"
                        if state == CORRECT_GUESS_STATE and not (unused_dothraki or unused_translations): # The win condition
                            state = WIN_STATE
                            earned_points += score                    
                            text = f"You won with a total of: {score} points, and \n the total earned points accross all games: {earned_points}"
                            if earned_points >= 50:
                                text += "\nReward:\nNominative (varies): Subject\nAccusative (—/-es): Direct Object\nGenitive (-i): Possessor\”Allative (-aan/-ea): Motion Towards\nAblative (-oon/-oa): Motion Away From"
                        writing = False
                        text_input = ""

                    elif POS_10_B.collidepoint(event.pos):
                        writing = not writing

            elif state == CORRECT_GUESS_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_9_B.collidepoint(event.pos):
                        choice = random.choices(["new", "translation"], [0.5, 0.5])[0]
                        if choice == "new" and unused_dothraki:
                            noun = unused_dothraki.pop(0)
                            used_dothraki.append(noun)
                            state = DORTHRAKI_NOUN_STATE
                        else:
                            state = TRANSLATION_STATE
                            if used_translations and random.choices([True, False],[0.25,0.75])[0] or not unused_translations: 
                                selected_word = random.choice(list(used_translations))  # Previously used translation
                            else:
                                selected_word = unused_translations.pop()  # New noun translation
                                used_translations.add(selected_word)

            elif state == LOST_STATE or WIN_STATE:
                if event.type == MOUSEBUTTONDOWN:
                    if POS_9_B.collidepoint(event.pos):
                        state = MAIN_MENU_STATE
                        score = 0
                        if earned_points >= 50:
                            gameData["rewardText"] = """
                            Nominative (varies): Subject
                            Accusative (—/-es): Direct Object
                            Genitive (-i): Possessor
                            Allative (-aan/-ea): Motion Towards
                            Ablative (-oon/-oa): Motion Away From
                            """
                        used_dothraki = []
                        used_translations = set()  
                        score = 0            
    pygame.quit()

game_loop()
