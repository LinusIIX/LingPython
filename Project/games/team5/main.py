#Letter Hunter (Ase Fonak) modification of Wormy by Sweigart
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
#Modified by Selin, Anna and Berrak and Tina- Anna's Data Science friend
# Python3.12 has been used to run this code
#The operating system used is Windows 11
# The camel case convention is parts from Sweigart's code and snake case convention is our own code.

#import the libraries
import random, pygame, sys
from pygame.locals import *
from assets import GameDataLink
gameData = GameDataLink.get_data()
gameData["neededPoints"] = 1
gameData["text"] = "This game is about collecting letters of dothraki words by eating them."
pygame.init() #initialize pygame
pygame.mixer.init() # initialize the mixer


FPS = 5 # changed speed frames per second
# changed the window width and height to 960 and 720
WINDOWWIDTH = 960
WINDOWHEIGHT = 720
CELLSIZE = 30 # changed the cell size to 30
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Colors from Sweigart's code and us
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKRED  = (139,   0,   0)
CRIMSON   = (220,  20,  60)
LIGHTRED  = (255,  99,  71)
GREEN     = (  0, 255,   0)
MINTGREEN = (152, 251, 152)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#Anna's code
# Define obstacles
obstacles = [
    # Points
    {'x': 10, 'y': 10},
    {'x': 15, 'y': 15},
    {'x': 20, 'y': 20},
    {'x': 25, 'y': 25},

    # Walls (horizontal and vertical lines)
    *[{'x': x, 'y': 5} for x in range(5, 15)],  # Horizontal wall
    *[{'x': 30, 'y': y} for y in range(10, 20)] # Vertical wall
]

HEAD = 0 # syntactic sugar: index of the worm's head

# Add a global variable to keep track of the current level
current_level = 'ESH'

def main(): #define main function  # Sweigart's and Selin's code
    global FPSCLOCK, DISPLAYSURF, BASICFONT, current_level

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Ase: Fonak ') # Set the window title

    show_Start_Screen()
    show_Instructions_Screen()
    while True:
        run_Game()
        show_Game_Over_Screen()


def run_Game(): #define runGame function
    global current_level

    initialize_level(current_level)# Initialize the current level

    # Set a random start point for worm ensuring it is not on an obstacle.
    while True:
        startx = random.randint(5, CELLWIDTH - 6) # set the x coordinate of the worm's head
        starty = random.randint(5, CELLHEIGHT - 6) # set the y coordinate of the worm's head
        wormCoords = [{'x': startx, 'y': starty},
                      {'x': startx - 1, 'y': starty},
                      {'x': startx - 2, 'y': starty}]
        if all(coord not in obstacles for coord in wormCoords):
            break
    direction = RIGHT

    # Start 3 letters at random locations
    letter1, letter2, letter3 = get_letters()

    while True:  # main game loop from lines 103 tp 118 is Sweigart's code
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit the obstacles, itself or the edges
        if wormCoords[HEAD] in obstacles: # check if the worm hit obstacles
            return show_Game_Over_Screen() # game over
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT: #Next 4 lines are Sweigart's code
            return show_Game_Over_Screen()# game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return show_Game_Over_Screen() # game over

        # Check if worm has eaten a letter
        #Check worm ate target letter
        if wormCoords[HEAD]['x'] == letter1['x'] and wormCoords[HEAD]['y'] == letter1['y']:
            # don't remove worm's tail segment
            collected_letters.append(letter1['char'])

            if level_completed():
                if collected_letters == list('ESH'): #words shortened for testing for better performance # First three letters of ESHIN
                    show_level_complete_screen('ESHIN', 'FISH')
                    current_level = 'EYE' #First three letters of EYELKI
                    letter1, letter2, letter3 = start_new_level(current_level)
                elif collected_letters == list('EYE'):
                    show_level_complete_screen('EYELKI', 'SPRING')
                    current_level = 'AHH' #First three letters of AHHAZ
                    letter1, letter2, letter3 = start_new_level(current_level)
                else:
                    return show_win_screen()
            else:
                # Set three new letters somewhere
                letter1, letter2, letter3 = get_letters()

        # Worm ate distraction letter
        elif wormCoords[HEAD]['x'] == letter2['x'] and wormCoords[HEAD]['y'] == letter2['y']:
            return show_wrong_letter_screen(letter2['char'])  # Show wrong letter screen

        elif wormCoords[HEAD]['x'] == letter3['x'] and wormCoords[HEAD]['y'] == letter3['y']:
            return show_wrong_letter_screen(letter3['char'])  # Show wrong letter screen

        # Worm did not eat any letter
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving #Next 8 lines are Sweigart's code
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1} # move the worm up
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1} # move the worm down
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']} # move the worm left
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']} # move the worm right
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        # draw the functions
        drawGrid()
        draw_obstacles(obstacles)
        drawWorm(wormCoords)
        draw_letter(letter1)
        draw_letter(letter2)
        draw_letter(letter3)
        draw_collected_letters()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
  


def drawPressKeyMsg(): # define draw press key function
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress(): #define checkForKeyPress function
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#Anna's code
def initialize_level(target_word): # define initialize level function
    global TARGET_WORD, DISTRACTION_LETTERS, collected_letters
    TARGET_WORD = list(target_word)
    DISTRACTION_LETTERS = "BCFGJMOPQRTU"  # sort letters for readability
    collected_letters = []
#Anna's code
def level_completed(): # define level completed function
    return len(TARGET_WORD) == 0
#Anna's code
def start_new_level(target_word): # define start new level function
    print("Starting new level with target word:", target_word)
    initialize_level(target_word)
    print("After function:", target_word)
    return get_letters()
#Selin's code
def play_Start_Music(): # add background music-a speech from the dothraki king Drogo
    pygame.mixer.music.load(r'material/drogos speech-game of thrones.mp3')
    pygame.mixer.music.play(-1, 7.0)  # Loop indefinitely, starting from the beginning after 7 seconds
    print("Start music playing!")
#Selin's code
def stop_Start_Music(): # Stop the music when game starts
    pygame.mixer.music.stop()
    print("Start music stopped!")

#Selin's code
def show_Start_Screen(): # define the start screen
    background_image = pygame.image.load(r'material/0b2829e1-f9b6-49a2-8248-6f6e26569f0b.webp')  #  add a path to the background image
    background_image = pygame.transform.scale(background_image, (960, 720))
    titleFont = pygame.font.Font(r'material/Cinzel-Bold.ttf', 90) #change the color and the font
    titleSurf = titleFont.render('ASE FONAK ', True, pygame.Color(220, 20, 60))
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 4)
# Press Key to start message
    pressKeyFont = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 40)  # change the color and font
    pressKeySurf = pressKeyFont.render('Press any key to start.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 1 - 30)

    play_Start_Music()  # Start the music

    lastBlinkTime = pygame.time.get_ticks()  # Time for blinking control
    blinkInterval = 500  # Time in milliseconds for the blink interval

    while True:
        DISPLAYSURF.blit(background_image, (0, 0))
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Check if it's time to blink the text
        currentTime = pygame.time.get_ticks()
        if (currentTime - lastBlinkTime) > blinkInterval:
            lastBlinkTime = currentTime  # Reset the timer
            pressKeySurf = pressKeyFont.render('Press any key to start.', True,
                                               WHITE if (currentTime // blinkInterval) % 2 == 0 else (0, 0, 0)) # Blinking text is white when the time is divisible by the blink interval, otherwise black

        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            break

        pygame.display.update()
        FPSCLOCK.tick(FPS)
#Selin's code
def show_Instructions_Screen(): #  define the instruction screen

    background_image = pygame.image.load(r'material/0b2829e1-f9b6-49a2-8248-6f6e26569f0b.webp') # add the path to the background image
    background_image = pygame.transform.scale(background_image, (960, 720))

    instructionsFont = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 30) # define the instructions
    instructions = [
        "Use arrow keys or WASD to move the worm.",
        "Collect the first three correct letters to form target words.",
        "Target words for each level: ESHIN, EYELKI, AHHAZ",
        "Avoid obstacles and distraction letters.",
        "Press ESC to quit the game."
    ]
    instructionsSurfs = [instructionsFont.render(line, True, pygame.Color(220, 20, 60), pygame.Color(0, 0, 0)) for line
                         in instructions]
    instructionsRects = [surf.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 4 + 100 + i * 40), ) for i, surf in
                         enumerate(instructionsSurfs)]
# Press Key to start message
    pressKeyFont = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 40) # define the font and color
    pressKeySurf = pressKeyFont.render('Press any key to start.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 1 - 30)

    lastBlinkTime = pygame.time.get_ticks() # Time for blinking control
    blinkInterval = 500

    while True:
        DISPLAYSURF.blit(background_image, (0, 0))
        for surf, rect in zip(instructionsSurfs, instructionsRects):
            DISPLAYSURF.blit(surf, rect)

# Handle blinking text in one place
        currentTime = pygame.time.get_ticks()
        if (currentTime - lastBlinkTime) > blinkInterval:
            lastBlinkTime = currentTime
            pressKeySurf = pressKeyFont.render('Press any key to start.', True,
                                               WHITE if (currentTime // blinkInterval) % 2 == 0 else (0, 0, 0)) # Blinking text is white when the time is divisible by the blink interval, otherwise black

        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            stop_Start_Music()
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Blink logic initialization

        blink_timer = 0   # Time tracker for blinking
        blink_interval = 1000  # Blinking interval in milliseconds
        last_blink_time = pygame.time.get_ticks()  # Get the initial time

# Show instructions and prompt to start game
    while True:
        DISPLAYSURF.blit(background_image, (0, 0))  # Blit the transparent overlay
        for surf, rect in zip(instructionsSurfs, instructionsRects):
            DISPLAYSURF.blit(surf, rect)
            DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        pygame.display.update()
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

        FPSCLOCK.tick(FPS)


def terminate(): # define terminate function
    GameDataLink.send_data(gameData) # Send the data to the server
    pygame.quit()
    sys.exit()


#Anna's code
def get_letters(): # Get first letter from ahhaz and two random distraction letters at random positions

    if len(TARGET_WORD) != 0:  # Get first letter from TARGET_WORD
        target_letter = TARGET_WORD.pop(0)
    else:
        return show_win_screen()

    # Get 2 random letter from DISTRACTION_LETTERS
    dist_letter1, dist_letter2 = random.sample(DISTRACTION_LETTERS, 2)

    # Get random positions for all letters and ensure they are not on top of each other
    positions = set()
    
    def get_unique_position(): # Get unique position for each letter
        while True:
            pos = (random.randint(0, CELLWIDTH - 1), random.randint(0, CELLHEIGHT - 1))
            if pos not in positions and pos not in [(obstacle['x'], obstacle['y']) for obstacle in obstacles]:
                positions.add(pos)
                return pos
# Get unique positions for each letter
    target_pos = {
        'x': get_unique_position()[0],
        'y': get_unique_position()[1],
        'char': target_letter
        }
    dist_pos1 = {
        'x': get_unique_position()[0],
        'y': get_unique_position()[1],
        'char': dist_letter1
        }
    dist_pos2 = {    
        'x': get_unique_position()[0],
        'y': get_unique_position()[1],
        'char': dist_letter2
        }
    
    return [target_pos, dist_pos1, dist_pos2]

#Berrak's code
def show_Game_Over_Screen(): # define game over screen
    font = pygame.font.Font(r'material/Cinzel-Bold.ttf', 80) # define the font and color
    gameOverSurf = font.render("Game Over", True, WHITE)
    gameOverRect = gameOverSurf.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))

    pressKeyFont = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 40)
    pressKeySurf = pressKeyFont.render('Press any key to retry.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 1 - 30))

    lastBlinkTime = pygame.time.get_ticks() # Time for blinking control
    blinkInterval = 500

    while True:
        DISPLAYSURF.blit(gameOverSurf, gameOverRect)

# Handle blinking text
        currentTime = pygame.time.get_ticks()
        if (currentTime - lastBlinkTime) > blinkInterval:
            lastBlinkTime = currentTime
            pressKeySurf = pressKeyFont.render('Press any key to retry.', True,
                                               WHITE if (currentTime // blinkInterval) % 2 == 0 else (0, 0, 0))

        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return  # Restart game

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
#Anna's code
def show_level_complete_screen(word, meaning): # Level complete screen
    font = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 40) # define the font and color
    textSurf = font.render("Correct! " + word + " means " + meaning + "!", True, MINTGREEN)
    textRect = textSurf.get_rect()
    textRect.midtop = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)

    DISPLAYSURF.blit(textSurf, textRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(2000)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return 

#Anna's code
def show_wrong_letter_screen(letter): #  define wrong letter screen
    font = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 40) # define the font and color
    textSurf = font.render(letter + " IS THE WRONG LETTER!", True, LIGHTRED)
    textRect = textSurf.get_rect()
    textRect.midtop = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)

    DISPLAYSURF.blit(textSurf, textRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(2000)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return run_Game()


def show_win_screen(): # define win screen
    letters = ['A', 'H', 'H', 'A', 'Z'] #define the target letters
    positions = [{'x': 15, 'y': 20}, {'x': 16, 'y': 20}, {'x': 17, 'y': 20}, {'x': 18, 'y': 20}, {'x': 19, 'y': 20}]
    wormCoords = [{'x': 0, 'y': 20}, {'x': -1, 'y': 20}, {'x': -2, 'y': 20}, {'x': -3, 'y': 20}, {'x': -4, 'y': 20}]
    direction = RIGHT

    new_letters = ['T', 'H', 'E', 'N'] #translation of the target letters
    new_positions = [{'x': 15, 'y': 20}, {'x': 16, 'y': 20}, {'x': 17, 'y': 20}, {'x': 18, 'y': 20}]
    letters_changed = False

    while wormCoords[-1]['x'] <= CELLWIDTH: # Move the worm to the end of the grid
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        newHead = {'x': wormCoords[0]['x'] + 1, 'y': wormCoords[0]['y']} # Move the worm to the right
        wormCoords.insert(0, newHead)
        

        if wormCoords[0]['x'] not in [pos['x'] for pos in positions]:   # Only grow the worm if it has eaten a letter
            wormCoords.pop()
        else:
            if wormCoords[0]['x'] == positions[-1]['x'] and not letters_changed: # Change the letters to THEN when worm reaches the last letter
                letters = new_letters
                positions = new_positions
                letters_changed = True

        DISPLAYSURF.fill(BLACK)
        font = pygame.font.Font(r'material/Merriweather-LightItalic.ttf', 50)
        text_surface = font.render("You did it! AHHAZ means... ", True, GREEN)
        text_rect = text_surface.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        DISPLAYSURF.blit(text_surface, text_rect)
        
        drawGrid()
        drawWorm(wormCoords)
        for i, letter in enumerate(letters):   # Draw each letter at its corresponding position
            draw_letter({'char': letter, 'x': positions[i]['x'], 'y': positions[i]['y']})
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    gameData["earnedPoints"] += 1
    gameData["rewardText"] = "Well done game finished, you learned that 'ahhaz' means 'then' / tl"
    pygame.time.wait(5000)
    terminate()

#Anna's code
def draw_collected_letters(): # Draw collected letters in the upper left corner:
    font = pygame.font.Font('freesansbold.ttf', 20)
    text_surface = font.render("Collected: " + "".join(collected_letters), True, WHITE)
    text_surface.set_alpha(128)  # Set transparency to 50%
    DISPLAYSURF.blit(text_surface, (10, 10))  # Top-left corner


def drawWorm(wormCoords): #function to draw the worm iterating over the three worm coord cells
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


#Anna's code
def draw_letter(letter): # function to draw the letter in the grid
    font = pygame.font.Font('freesansbold.ttf', 25) # default font
    text_surface = font.render(letter['char'], True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (letter['x'] * CELLSIZE + 5, letter['y'] * CELLSIZE + 5)
    DISPLAYSURF.blit(text_surface, text_rect)

#Anna's code
def draw_obstacles(obstacles): # Draw obstacles in the grid
    for obstacle in obstacles:
        x = obstacle['x'] * CELLSIZE # multiply the vertical obstacle by the cell size
        y = obstacle['y'] * CELLSIZE # multiply the horizontal obstacle by the cell size
        obstacleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKRED, obstacleRect)


def drawGrid(): #draw grid
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


#execute main function
if __name__ == '__main__':
    main()