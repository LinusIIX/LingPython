"""
Project: Dothraki Noun Game
Collaborators: Celil Durna, Dafina Kastrati


Work Distribution:

- Game Data & Setup                         -> Celil
- Display (window & fps control)            -> Celil
- Images (loading & setup)                  -> Dafina
- Spaceship (player mechanics)              -> Celil
- Laser (shooting & mechanics)              -> Celil
- Meteor (Spawning, Movement, Rotation)     -> Dafina
- Dust (explosion effect)                   -> Dafina
- Dust Cloud Group (Management)             -> Dafina

Helper Functions for Main Game:
- Spawning meteors (spawn_meteors)          -> Dafina
- Game state reset (resetGameState)         -> Celil
- Background music handling                 -> Dafina
- Processing user input (processInput)      -> Celil
- Updating game objects (updateGameObjects) -> Celil
- Score display & timer functions           -> Dafina
- Rendering game window (drawGameWindow)    -> Dafina

Main Game:
- Core Game Loop                            -> Both (equal contribution)
- Game Mechanics debugging                  -> Both
- Collision handling & score updates        -> Celil
- Hint unlocking system                     -> Celil

Menus:
- Start Menu (design & functionality)       -> Dafina
- End Menu (game over & score display)      -> Dafina

Note: We worked together as a team and contributed equally overall. Some sections were developed individually, 
      but we also worked together at the same laptop, especially on core gameplay mechanics.
"""


import pygame
import sys # for stopping the game -> sys.exit
import time
import math 
import random
from os import path # to get file paths -> for loading images and music
from assets import GameDataLink  # for connection to GameEngine

# load game state data from the Game Engine
gameData = GameDataLink.get_data()
gameData["neededPoints"] = 5
gameData["text"] = "you have to hit 100 meteorites in 50 seconds to win the game"

img_path = path.join(path.dirname(__file__), 'images') # path to the images folder
msc_path = path.join(path.dirname(__file__), 'music')  # path to the music folder

pygame.init() # initialize pygame



################ Display ##################################################################################

# this class manages the game window (1280x720) and frame rate control 
class  Display():
    def __init__(self, width=1280, height=720, title="Dothraki Noun Game"):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height)) # create the game window
        pygame.display.set_caption(title) # set the window title
        self.clock = pygame.time.Clock() # initialize a clock to control the frame rate

display = Display() # create a display instance that will be used for the startmenu, endmenü, and the game



################ Images ###################################################################################

# get all game images -> background, spaceship (=player), meteor

# load the background image
# source: https://www.reddit.com/r/PixelArt/comments/dg2vec/i_created_this_full_hd_pixel_art_wallpaper_for_my/
background = pygame.image.load(path.join(img_path, 'background.png')).convert()

# load the spaceship (=player) image
# source: https://pixelartmaker.com/art/3250a02b1f65bd7
img_spaceship = pygame.image.load(path.join(img_path, 'spaceship.png')).convert() #lila gut

# load the meteor image
# source: https://www.pixil.art/art/astrode-sr2d0da3123adaws3?ft=user&ft_id=1961395
img_meteor = pygame.image.load(path.join(img_path, 'meteor.png')).convert() 



################ Spaceship ################################################################################

# this class represents the player i.e the spaceship in the game
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()  

        # load and resize the spaceship image
        self.image = pygame.transform.scale(img_spaceship, (85, 75)) 
        self.image.set_colorkey((0, 0, 0)) # remove black background for transparency

        # define the hitbox of the player and collision detection
        self.rect = self.image.get_rect()
        self.radius = 25 # for collision detection

        # Set the initial position at the bottom center of the display
        self.rect.center = (display.width // 2, 680)

        # player movement speed
        self.vel = speed

        # score tracking
        self.score = 0



################ Laser ####################################################################################

# this class represents a laser fired by the player i.e the spaceship (to hit the meteorites)
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-15):
        super().__init__() 

        # create a simple laser shape and set its color
        self.image = pygame.Surface((5, 20)) # size (5x20)
        self.image.fill((255, 0, 255)) # pink-violett color

        # define the hitbox of the laser and position
        self.rect = self.image.get_rect()
        self.rect.center = x
        self.rect.bottom = y

        # laser speed (default -15, moves upwards)
        self.speed_y = speed

    # this function moves the laser upwards and remove it when it goes off-screen
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()



################ Meteor ###################################################################################

# this class represents an meteor falling towards the player i.e spaceship
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 

        # load and resize the meteor image
        self.sizes = [[50, 50], [65, 65], [80, 80], [95, 95], [110, 110], [125, 125]] # possible sizes
        self.image_original = pygame.transform.scale(img_meteor, random.choice(self.sizes))
        self.image_original.set_colorkey((0, 0, 0)) # remove black background
        self.image = self.image_original.copy() # store a copy for rotation effects

        # define the hitbox of the meteorites and collision detection
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)  # collision radius

        # spawn the meteor at a random horizontal position above the screen
        self.rect.x = math.floor(random.randrange(-4, display.width))
        self.rect.y = math.floor(random.randrange(-10, -2))

        # random movement speed
        self.speed_y = math.floor(random.randrange(3, 5)) # vertical falling speed
        self.speed_x = math.floor(random.randrange(-4, 6)) # horizontal drift

        # random rotation speed
        self.rot = 1 # initial rotation angle
        self.rot_speed = random.randrange(-7, 7) # random rotation speed

    # this function rotate the meteor continuously to create a spinning effect
    def rotate(self):
        self.rot += self.rot_speed % 360 # keep rotation within 0-359 degrees
        new_image = pygame.transform.rotate(self.image_original, self.rot) # rotate the meteor
        old_center = self.rect.center # store the current center position
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center # restore the center position after rotation

    # this function moves and rotates the meteor, reset position when it leaves the screen
    def update(self):
        self.rotate() # apply rotation effect
        self.rect.x += self.speed_x # apply horizontal movement
        self.rect.y += self.speed_y # apply vertical movement

        # reset meteor if it moves out of the screen
        if (self.rect.x < 0) or (self.rect.x > display.width) or (self.rect.y > display.height):
            self.rect.x = math.floor(random.randrange(0, display.width)) # reposition at a new random x location
            self.rect.y = math.floor(random.randrange(-4, -2)) # spawn back above the screen
            self.speed_y = math.floor(random.randrange(2, 7)) # assign a new falling speed



################ DUST #####################################################################################

# this class represents small dust clouds (/explosion) effect when meteors are destroyed
class Dust(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # create a small transparent surface for the dust effect
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)  # transparent background using SRCALPHA -> Enables per-pixel transparency (RGBA mode)
        self.color = (87, 87, 87)  # grey color (same as meteor)
        pygame.draw.circle(self.image, self.color, (3, 3), 3)  # draw a circle

        # hitbox and position of the dust 
        self.rect = self.image.get_rect()
        self.rect.x = x  # set the horizontal position
        self.rect.y = y  # set the vertical position

        # movement 
        self.vel_x = random.randint(-3, 3)  # random horizontal spread
        self.vel_y = random.randint(-8, -1)  # moves upward slightly
        self.lifetime = 30  # number of frames before disappearing

    # this function moves the dust cloud and removes it when lifetime ends
    def update(self):
        self.rect.x += self.vel_x # apply horizontal movement
        self.rect.y += self.vel_y # apply vertical movement
        self.lifetime -= 1  # reduce lifetime with each frame

        # remove the dust cloud when its lifetime reaches 0
        if self.lifetime <= 0:
            self.kill()

    # this function draws the dust cloud on the screen
    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.pos_x), int(self.pos_y)), self.rad)



################ DUST CLOUD GROUP #########################################################################

dust_clouds = pygame.sprite.Group()  

# this function generate 20 dust clouds at the given position
def createDustCloud(x, y):
    for _ in range(15):
        dust = Dust(x, y)
        dust_clouds.add(dust)  # add to the sprite group

# this function update and draw all dust clouds
def updateAndDrawDust(surf):
    dust_clouds.update()  # move and remove dust clouds when their lifetime end
    dust_clouds.draw(surf)  # automatically draws all active dust clouds



################ Helper Functions for Main Game ###########################################################

# this fuction creates a specified number of meteors and adds them to the meteor group -> for creating meteors at start of game
def spawn_meteors(count=10):
    for _ in range(count):
        meteors.add(Meteor()) 


# this function resets the game state by reinitializing all objects and groups
def resetGameState():
    # global variables -> store key game objects (player, meteors, lasers, and all sprites)
    # they need to be accessible and updated across multiple functions like game resets, object updates, and event handling
    # without global, changes inside functions would not reflect in the actual game state, causing inconsistent behavior
    global player, all_sprites, meteors, lasers 

    player = Spaceship(10) # create player instance

    # reset the global variables:
    all_sprites = pygame.sprite.Group() # group for all game objects (player/spaceship, meteors, lasers)
    meteors = pygame.sprite.Group() # group for meteors
    lasers = pygame.sprite.Group() # group for lasers

    all_sprites.add(player) # add player to main group

    spawn_meteors(10)  # spawn a new set of meteors at the beginning of the game

    player.score = 0 # reset player score
    gameData["earnedPoints"] = 0  # reset earned points to 0 to ensure a fresh start after restart
    #triggered_hints.clear() # not important


# this function initializes and starts the background music for the game
def startBackgroundMusic():
    pygame.mixer.init() # initialize the pygame mixer for audio playback
    pygame.mixer.music.load(path.join(msc_path, '20min.mp3')) # load the background music file
    pygame.mixer.music.set_volume(0.1) # set the music volume to 10%
    pygame.mixer.music.play(-1) # play the music in an infinite loop


# this function handles user inputs (movement, shooting, quitting the game)
def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() # exit the game when the close button is clicked
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # create a laser when the player presses ENTER and add it to the game
            laser = Laser(player.rect.center, player.rect.top)
            all_sprites.add(laser)
            lasers.add(laser)


# this function updates all game objects and checks for collisions
# -> handles player movement, updates all sprites, processes laser-meteor collisions, and checks if the player reaches score thresholds or gets hit by a meteor
def updateGameObjects():
    global triggered_hints

    # handle player movement based on key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.x > 0:
        player.rect.x -= player.vel # move left (A)
    if keys[pygame.K_d] and player.rect.x < display.width - 80:
        player.rect.x += player.vel # Move right (D)

    # update all game objects
    all_sprites.update()
    meteors.update()

    # check if a laser hits a meteor
    hits = pygame.sprite.groupcollide(lasers, meteors, True, True)
    for hit in hits:
        createDustCloud(hit.rect.x, hit.rect.y) # create explosion effect
        meteor = Meteor() # spawn a new meteor
        meteors.add(meteor)
        player.score += 1 # increase player score

    # check if the player reaches score thresholds for hints
    thresholds = {
        20: "There are 3 nouns in the sentence.",
        40: "The nouns are 'eshin', 'yette', 'eyelki'.",
        60: "'eshin' means 'fish'.",
        80: "'yette' means 'frog'.",
        100: "'eyel' means 'rain'."
    }

    if player.score in thresholds and player.score not in triggered_hints:
        gameData["earnedPoints"] = sum(1 for t in thresholds if player.score >= t) # Calculate the exact number of earned poinzt i.e hints based on score
        gameData["rewardText"] = thresholds[player.score] # set the hint message (rewardText)
        GameDataLink.send_data(gameData) # send updated game data
        triggered_hints.add(player.score) # mark this threshold as reached

        # if the player reaches 100 points -> win the game
        if player.score == 100:
            endMenu(reason="win")

    # check if a meteor collides with the player
    if pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle):
        endMenu(reason="died") # end the game if the player is hit


# this function displays the current score on the screen -> top center
def displayScore(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('verdana'), size) # load the Verdana font with the given size
    font.set_bold(True) # make the font bold for better visibility
    textSurface = font.render(text, True, (255, 255, 255)) # render the text in white color
    textArea = textSurface.get_rect() # get the bounding box of the text
    textArea.midtop = (x, y) # position the text at the given coordinates
    surf.blit(textSurface, textArea) # draw the text onto the screen


# this fuction displays the remaining game time on the screen -> top left
def displayTimer(surf, time_left, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('verdana'), size) # load the Verdana font with the given size
    color = (255, 0, 0) if time_left <= 5 else (255, 255, 255) # set text color to red if time is 5 seconds or less, else white
    textSurface = font.render(f'Time: {time_left}', True, color) # render the timer text with the selected color
    textArea = textSurface.get_rect() # get the bounding box of the text
    textArea.midtop = (x, y) # position the text at the given coordinates
    surf.blit(textSurface, textArea) # draw the text onto the screen


# this function renders the game window, updates the background, and displays game information
def drawGameWindow(remaining_time):
    display.window.fill((0, 0, 0)) # fill the screen with black to clear the previous frame
    display.window.blit(pygame.transform.scale(background, (display.width, display.height)), (0, 0)) # draw the background image scaled to fit the screen

    updateAndDrawDust(display.window) # update and render dust particle effects
    
    all_sprites.draw(display.window) # draw all active game sprites (player, lasers, ...)
    meteors.draw(display.window) # draw all meteors on the screen

    displayScore(display.window, 'Score: ' + str(player.score), 40, 640, 10) # display the score of playee
    displayTimer(display.window, remaining_time, 30, 100, 15) # show the timer

    pygame.display.update() # refresh the screen with the updated game frame



################ Main Game ################################################################################

triggered_hints = set() # a set to keep track of hints that have already been triggered

# main game function that initializes, updates, and renders the game
def mainGame():
    global player, all_sprites, meteors, lasers  

    # initialize game objects and sprite groups
    resetGameState()

   # start background music
    startBackgroundMusic()

    # record the starting time of the game
    start_time = time.time()  

    # main game loop
    while True:
        display.clock.tick(60) # limit the game loop to 60 fps
        elapsed_time = time.time() - start_time # calculate elapsed time since game start
        remaining_time = max(0, 50 - int(elapsed_time)) # countdown from 50 seconds

        # handle user inputs (movement, shooting, quitting)
        processInput()
        
        # update all game objects (movement, collisions, score tracking)
        updateGameObjects()

        # rendering function -> draw the updated game frame
        drawGameWindow(remaining_time)

        # check if the game should end because time end
        if elapsed_time >= 50:
            endMenu(reason="time") # show end menu

    pygame.quit() # ensure the game closes properly
    sys.exit() # exit the program



################ End Menu #################################################################################

# this function displays the end menu with the final score and unlocked hints
def endMenu(reason="died"):

    # stop the background music
    pygame.mixer.music.stop() 

    # renders text on the screen (with adjustable font size, position, color, and alignment)
    def showText(surf, text, size, x, y, color=(255, 255, 255), bold=False, align="center"):
        font = pygame.font.Font(pygame.font.match_font('Verdana', False), size)
        if bold:
            font.set_bold(True)
        textSurface = font.render(text, True, color)

        if align == "center":
            textRect = textSurface.get_rect(center=(x, y))  # center alignment
        else:
            textRect = textSurface.get_rect(topleft=(x, y))  # left alignment

        surf.blit(textSurface, textRect) # draw text on the screen


    # determine the title text based on the reason for game over
    if reason == "win":
        title_text = "You Win!"
    elif reason == "time":
        title_text = "Time is Over!"
    else:
        title_text = "You Died!"

    # list of unlocked hints based on the final score
    unlocked_hints = []
    if player.score >= 20:
        unlocked_hints.append("Hint 1: There are 3 nouns in the sentence.")
    if player.score >= 40:
        unlocked_hints.append("Hint 2: The nouns are 'eshin', 'yette', 'eyelki'.")
    if player.score >= 60:
        unlocked_hints.append("Hint 3: 'eshin' means 'fish'.")
    if player.score >= 80:
        unlocked_hints.append("Hint 4: 'yette' means 'frog'.")
    if player.score >= 100:
        unlocked_hints.append("Hint 5: 'eyel' means 'rain'.")

    while True:
        display.clock.tick(60) # limit to 60 fps

        # handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # close the game if the window is closed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # exit game
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE: # restart game
                    mainGame()

        # fill the background black
        display.window.fill((0, 0, 0))

        # title (yellow, large font)
        showText(display.window, title_text, 48, display.width // 2, 80, (255, 215, 0), bold=True)

        # score (white, bold)
        showText(display.window, f"Score: {player.score}", 38, display.width // 2, 140, (255, 255, 255), bold=True)

        # display the sentence (light blue -> similar to the start menu)
        showText(display.window, 'Sentence: "ezatas ma eshin ma yette she eyelki chosh"', 30, display.width // 2, 220, (173, 216, 230))

        # "Unlocked Hints" title (white, bold + smaller than score)
        showText(display.window, "Unlocked Hints:", 30, display.width // 2, 270, (255, 255, 255), bold=True)

        # position for unlocked hints
        hints_x = display.width // 2 - 270  # left-aligned 
        y_offset = 300  # start position for hints 

        # display all unlocked hints (white text, normal size)
        for hint in unlocked_hints:
            showText(display.window, f"- {hint}", 26, hints_x, y_offset, (255, 255, 255), align="left")
            y_offset += 50  # space between hints

        # final line -> Restart or Exit (green, bold, with extra spacing after hints)
        showText(display.window, "Press SPACE to restart or ESC to quit", 28, display.width // 2, y_offset + 45, (50, 205, 50), bold=True)

        pygame.display.update() # refresh the screen



################ Start Menu ###############################################################################

# this function displays the start menu -> game instructions and for starting the game
def startMenu():
    # renders text on the screen (with adjustable font size, position, color, and alignment)
    def showText(surf, text, size, x, y, color=(255, 255, 255), bold=False, align="center"):
        font = pygame.font.Font(pygame.font.match_font('Verdana', False), size)
        if bold:
            font.set_bold(True)
        textSurface = font.render(text, True, color)

        if align == "center":
            textRect = textSurface.get_rect(center=(x, y))  # center alignment
        else:
            textRect = textSurface.get_rect(topleft=(x, y))  # left alignment

        surf.blit(textSurface, textRect) # draw text on the screen

    while True:
        display.clock.tick(60) # limit to 60 fps

        # handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # close the game if the window is closed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # start the game when SPACE is pressed
            mainGame()

        # fill the background black
        display.window.fill((0, 0, 0))

        # title of the game (yellow, large font)
        showText(display.window, 'Welcome to the Dothraki Noun Game!', 38, display.width // 2, 50, (255, 215, 0), bold=True)

        # display the sentence to be analyzed (light blue)
        showText(display.window, 'Sentence: "ezatas ma eshin ma yette she eyelki chosh"', 26, display.width // 2, 100, (173, 216, 230))

        # brief game objective (white)
        showText(display.window, 'Your goal: Learn the nouns from this sentence', 24, display.width // 2, 135, (255, 255, 255))

        # space between sections
        block_spacing = 50  # Space between sections

       # gameplay instructions title (white, bold)
        showText(display.window, 'How to Play:', 30, display.width // 2, 180, (255, 255, 255), bold=True)

        # positioning for instructions (left-aligned for bullet points)
        instructions_x = display.width // 2 - 200  

        # instructions for gameplay 
        showText(display.window, '- Move left with [A] and right with [D].', 24, instructions_x, 210, align="left")
        showText(display.window, '- Shoot meteors with [ENTER].', 24, instructions_x, 240, align="left")
        showText(display.window, '- Every hit gives you +1 Score.', 24, instructions_x, 270, align="left")
        showText(display.window, '- You have 50 seconds!', 24, instructions_x, 300, align="left")
        showText(display.window, '- Avoid meteors! If one hits you, you lose.', 24, instructions_x, 330, align="left")  

        # space before the hint section
        showText(display.window, '', 1, display.width // 2, 330 + block_spacing)  # Invisible text to add space

        # information about unlocking hints (white, bold)
        showText(display.window, 'Hints for nouns are unlocked at specific scores:', 28, display.width // 2, 400, (255, 255, 255), bold=True)

        # list of score thresholds and corresponding hints
        y_offset = 430
        hints = [
            ("20  Points", "1 Hint"),
            ("40  Points", "2 Hints"),
            ("60  Points", "3 Hints"),
            ("80  Points", "4 Hints"),
            ("100 Points", "5 Hints (You win!)")
        ]

        for points, hint_text in hints:
            showText(display.window, f"- {points:<8} --> {hint_text}", 24, instructions_x, y_offset, align="left")
            y_offset += 30  # space between hints

        # space before start prompt
        showText(display.window, '', 1, display.width // 2, y_offset + block_spacing)  

        # prompt to start the game (green, bold)
        showText(display.window, 'Press SPACE to start', 30, display.width // 2, y_offset + 50, (50, 205, 50), bold=True)

        pygame.display.update()



################ Run Game #################################################################################
# start game
startMenu()

# close game
pygame.quit()