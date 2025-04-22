"""
------ Linguistic Gaming with Python -----
----------- Dothraki word order ----------
project by:
- Lettie Topping lettie.topping@uni-kosnatanz.de - 01/1467138
- Lorenzo Severini lorenzo.severini@uni-konstanz.de - 01/1484414

		Lorenzo's sources: i) https://youtu.be/AY9MnQ4x3zk?si=_kt92jt4QSMHtpJi
        music from: https://youtu.be/vS_eeF2io_g?si=ls_KDEmcstRRW2dX
        artworks: 
            - map by MrBeast (https://opengameart.org/content/cave-tileset-0)
            - paper textutre background for dictionary: https://www.shutterstock.com/image-illustration/old-paper-texture-pixel-art-vintage-1808624245
            - all other artworks (characters, npc, objects) were drawn by Lorenzo
            - Dothraki alphabet adapted from https://www.omniglot.com/conscripts/dothraki.htm

> code run on MacBook Pro 2024 with MacOS Sequoia 15.3, 
> python version: Python 3.13.1 -- pygame version: pygame 2.6.1
"""

## IMPORTANT: all paths for files have been edited as .../file.extension in order to work in the overall work made by Luca Pomm and colleagues



import pygame
from sys import exit
import random

from assets import GameDataLink

gameData = GameDataLink.get_data()
gameData["neededPoints"] = 3
gameData["text"] = "Guess all the Dothraki word orders."

def player_choice(character):
    ### function to choose the player character
    # the function is passed an argument which represent the desired character
    # depending on the argument, either the female character or the male character graphics are imported
    # two sets of graphics are imported, each consisting of 4 frames: i) idle character, ii) running character
    # imported animations are scaled
    # then a variable player is created: it refers to a list of two lists: the two embedded lists are a list of the character's animation in the different chartacter states
    # eventually game_active is set to true, so that the intro screen can be exited and the game can start

    global player, game_active

    if character == "F":
        # PLAYER F
        player_idle0 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_idle0.png').convert_alpha()
        player_idle1 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_idle1.png').convert_alpha()
        player_idle2 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_idle2.png').convert_alpha()
        player_idle3 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_idle3.png').convert_alpha()
        player_idle0 = pygame.transform.scale(player_idle0,(16*4,16*4)) # scale imported image
        player_idle1 = pygame.transform.scale(player_idle1,(16*4,16*4))
        player_idle2 = pygame.transform.scale(player_idle2,(16*4,16*4))
        player_idle3 = pygame.transform.scale(player_idle3,(16*4,16*4))

        #change for female input
        player_run0 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_run0.png').convert_alpha()
        player_run1 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_run1.png').convert_alpha()
        player_run2 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_run2.png').convert_alpha()
        player_run3 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerF_run3.png').convert_alpha()
        player_run0 = pygame.transform.scale(player_run0,(16*4,16*4))
        player_run1 = pygame.transform.scale(player_run1,(16*4,16*4))
        player_run2 = pygame.transform.scale(player_run2,(16*4,16*4))
        player_run3 = pygame.transform.scale(player_run3,(16*4,16*4))

    elif character == "M":
        # PLAYER M
        player_idle0 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_idle0.png').convert_alpha()
        player_idle1 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_idle1.png').convert_alpha()
        player_idle2 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_idle2.png').convert_alpha()
        player_idle3 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_idle3.png').convert_alpha()
        player_idle0 = pygame.transform.scale(player_idle0,(16*4,16*4))
        player_idle1 = pygame.transform.scale(player_idle1,(16*4,16*4))
        player_idle2 = pygame.transform.scale(player_idle2,(16*4,16*4))
        player_idle3 = pygame.transform.scale(player_idle3,(16*4,16*4))

        player_run0 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_run0.png').convert_alpha()
        player_run1 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_run1.png').convert_alpha()
        player_run2 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_run2.png').convert_alpha()
        player_run3 = pygame.image.load('games/lettie_lorenzo/graphics/player/playerM_run3.png').convert_alpha()
        player_run0 = pygame.transform.scale(player_run0,(16*4,16*4))
        player_run1 = pygame.transform.scale(player_run1,(16*4,16*4))
        player_run2 = pygame.transform.scale(player_run2,(16*4,16*4))
        player_run3 = pygame.transform.scale(player_run3,(16*4,16*4))

    # player[0] == idle animations
    # player[1] == run animations
    player = [[player_idle0,player_idle1,player_idle2,player_idle3],[player_run0,player_run1,player_run2,player_run3]]

    game_active = True

def player_animation():
    ### function to animate player in two different scenarios:
    #   1. walking: when KEYDOWN input is detected the player surface is chosen among the running animations
    #   2. idle: when no KEYDOWN input is detected the player surface is choosen among the idle animations
    # the animation images are stored in a list which contains two lists:
    #   player[0]: list containing idle animations
    #   player[1]: list containing running animations
    # an index is created and it is increased minimally (+=0.1) in each frame (call to function)
    # the index is considered in integers, thus avoiding all numbers with a comma
    # the index will refer to the position in one of the two lists so that a different animated position is chosen for the player
    # the chosen animated position will be used as the player surface

    global player_surf, player_index

    # get keyboard input
    keys = pygame.key.get_pressed()
    # defined movement input
    movement_keys = {pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}
    # check whether keyboard input is among movement input
    if any(keys[key] for key in movement_keys):
        player_index += 0.1
        if player_index >= len(player[1]): player_index = 0 # if index grows bigger than list with animations then it is set back to 0
        player_surf = player[1][int(player_index)] # update player surface with integer from gowing index
    else:
        player_index += 0.1
        if player_index >= len(player[0]): player_index = 0
        player_surf = player[0][int(player_index)]

def player_move():
    ### function to move player around the screen
    # get player input by creating a variable keys which is a dictionary of format: {key_x:True/False} where T/F indicate whether a specific key is being pressed
    # check whether a certain move key is being pressed: arrows and WASD work the same
    # if a move key is being pressed, then player rectangle x or y axis is updated by 4 pixels in the respective direction
    # orientation is changed only if left or right keys are pressed; current orientation is maintained if up or down keys are pressed
    # after movement, player_rect is checked for collision with boundary rectangles: if collision then player_rect position is adjusted back by 5px (bouncing effect)

    global player_orientation

    keys = pygame.key.get_pressed()

    # movement left
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_orientation = "Left"
        player_rect.x -= 4
        # checking for collision with a border rectangle
        if any(player_rect.colliderect(rect) for rect in border_rects):
            player_rect.left+=5

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_orientation = "Right"
        player_rect.x += 4
        if any(player_rect.colliderect(rect) for rect in border_rects):
            player_rect.right-=5

    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= 4
        if any(player_rect.colliderect(rect) for rect in border_rects):
            player_rect.top+=5

    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += 4
        if any(player_rect.colliderect(rect) for rect in border_rects):
            player_rect.y-=5

def npc_animation():
    ### function to animate the NPC in only one scenario (idle)
    # same process as player animation

    global npc_surface, npc_index

    npc_index += 0.09 # 0.01 less than player_index, it looks more natural to have different animation times between the characters
    if npc_index >= len(npc[0]): npc_index = 0
    npc_surface = npc[0][int(npc_index)]

def show_dict():
    ### function to show dictionary in two different places:
    #   1. on the floor when inventory==[]
    #   2. on top-left corner for access when inventory==["dictionary"] (aka it has been picked up)
    # function allows to access dictionary screen from different screens: needed when the minigame is active
    # show_dict_message runs only the first time that a collision is detected in order to give player instructions on how to use the dictionary

    global show_dict_message

    if "dictionary" not in inventory:
        dictionary_rect.center = (150,300)
        SCREEN.blit(dictionary_surf,dictionary_rect)
    elif "dictionary" in inventory:
        dictionary_rect.center = (40,40)
        SCREEN.blit(dictionary_surf,dictionary_rect)
        if show_dict_message == True:
            SCREEN.blit(open_dictionary_text,open_dictionary_text_rect) # instructions

def npc_conversation():
    ### function to show instructions on how to start the conversation with the npc
    # show_dict_message needs to be false otherwise there would be overlapping text
    if show_dict_message == False:
        SCREEN.blit(start_conversation_text,start_conversation_text_rect)

def talk():
    ### function to start conversation with player in two scenarios:
    #   1. if inventory==['dictionary'] : leads to minigame
    #   2. if inventory==[] : npc prompts the player to collect the dictionary first
    # minigame_active is the variable which, when True, starts the minigame in the game loop
    # if no mouse press is detected on conversation cloud then conversation instructions are showed

    global minigame_active, instruction_count, pregame_instruction
    if talk_to_npc: # this is true only when a collision between mouse press and conversation cloud is detected
        if "dictionary" in inventory:
            # shows minigame isntructions as a dialogue
            # instructions are contained in a list, depending on the point at which the dialogue is different positions in the list are printed
            if instruction_count<=len(pregame_instruction)-1:
                instruction = corpus_font.render(pregame_instruction[instruction_count],False,"White")
                instruction_rect = instruction.get_rect(center = (400,30))
                SCREEN.blit(instruction,instruction_rect)
                dialogue_cloud_rect.center = instruction_rect.center
                dialogue_cloud_rect.x = instruction_rect.right+5 # dialogue cloud follows the text
                SCREEN.blit(dialogue_cloud,dialogue_cloud_rect)

            else: minigame_active = True
        else:
            SCREEN.blit(conversation_0,conversation_0_rect)
    else: npc_conversation() # instructions

def win():
    ### function that allows player victory after the minigame is completed
    # for the winning condition the npc moves out of the way to let the player pass
    # to move the npc:
    #   position of npc is cheked against the target: if lower (aka target not reached) npc is moved of step
    #                                                 when npc reaches target, npc_move is set back to False
    #   this is necessary to give the impression of the npc moving because the function works little by little across multiple frames

    global npc_move, npc_orientation

    SCREEN.blit(win_text,win_text_rect) # winning line
    
    if npc_surf_rect.x < target:
        npc_surf_rect.x += step
    elif npc_surf_rect.x >= target:
        npc_move = False
        npc_orientation = "Left"


#/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Lettie

def call_dictionary():
    ### function to display the contents of the dictionary
    # letters is a dictionary in the form {dothranki_letter_surface:'english_letter'}
    # loops through each of the dothraki characters, creates a rectangle, and blits it further down the screen
    # blits the English letter 100 pixels to the right of the dothraki letter

    SCREEN.blit(dict_surf, (0,0))
    x = 50
    y = 50
    n = 0

    for d,e in letters:
        n += 1
        letter_rect = d.get_rect(center = (x, y))
        SCREEN.blit(d,letter_rect)

        text = dictionary_font.render('-  ' + e, True, 'Black')
        text_rect = text.get_rect(center = (x+100, y))
        SCREEN.blit(text,text_rect)

        y += 75
        if n == 10:
            x = 300
            y = 50
        if n == 20:
            x = 600
            y = 50

def call_minigame():
    ### function that displays the mini-game basics
    # checks what level the players is on, and displays the relevant text in dothraki
    # level 1: main clause // level 2: question // level 3: subordinate clause

    global level, guess, minigame_active, npc_move

    SCREEN.blit(scroll_surf, (0,0))

    if level <= 3: active = True # continues until level number is 1,2,3
    else: active = False

    if active:
        # Redraw letters after updating their position
        for letter in displayed_letters:
            SCREEN.blit(letter[0], letter[1])

        if level == 1:

            display_level_text(1)

            if len(guess) == 3:
                SCREEN.blit(check_text,check_text_rect)
                if check_answer: check(guess, ANSWER_1)

        elif level == 2:

            display_level_text(2)

            if len(guess) == 3:
                SCREEN.blit(check_text,check_text_rect)
                if check_answer:check(guess, ANSWER_2)

        elif level == 3:

            display_level_text(3)

            if len(guess) == 3:
                SCREEN.blit(check_text,check_text_rect)
                if check_answer:check(guess, ANSWER_3)

    else:
        # All levels complete
        minigame_active = False
        npc_move = True

def reset():
    ### function that displays the characters you can choose from for the minigame
    # Blits dothraki versions of SOV, and 7 random others in random positions on the screen

    global displayed_letters

    if level <= 3:
        coords = [(250,220), (325, 220), (400,220), (475,220), (550,220), (250,280), (325,280), (400,280), (475,280), (550,280)]
        incorrect_letters = INCORRECT_LETTERS.copy() #??
        displayed_letters = []

        # SOV characters
        for letter in ANSWER_1:
            coord = random.choice(coords)
            letter_rect = letter.get_rect(center = coord)
            SCREEN.blit(letter, letter_rect)
            coords.remove(coord)
            displayed_letters.append([letter, letter_rect, coord])

        # rest of the characters
        for x in range(len(coords)):
            coord = random.choice(coords)
            letter = random.choice(incorrect_letters)
            incorrect_letters.remove(letter)
            letter_rect = letter.get_rect(center=coord)
            SCREEN.blit(letter, letter_rect)
            coords.remove(coord)
            displayed_letters.append([letter,letter_rect, coord])

def check(player_guess, correct_answer):
    ### function that compares the player's guess to the answer
    # if the guess is correct, move onto the next level
    # if the guess is incorrect puts the dothraki letters back in their original position

    global level, check_answer, attempts

    attempts += 1
    check_answer = False

    #correct
    if player_guess == correct_answer:
        gameData["earnedPoints"]+=1
        level += 1
        attempts = 0
        guess.clear()
        reset()

    # incorrect
    else:
        guess.clear()
        for letter in displayed_letters:
            letter[1].center = letter[2]
            SCREEN.blit(letter[0], letter[1])

def display_level_text(level):
    #displays a hint if number of attempts is more than 5

    if attempts >= 5:
        SCREEN.blit(hint_text_1, hint_text_1_rect)
        SCREEN.blit(hint_text_2,hint_text_2_rect)

    if level == 1:
        ### function that blits 'main clause' in dothraki

        x = 335
        y = 500

        for e in main_text:
            e_rect = e.get_rect(center=(x, y))
            SCREEN.blit(e, e_rect)
            x += 40

        x = 275
        y = 550

        for e in clause_text:
            e_rect = e.get_rect(center=(x, y))
            SCREEN.blit(e, e_rect)
            x += 50

    elif level == 2:
        ### function that blits 'question' in dothraki

        x = 275
        y = 500

        for e in question_text:
            e_rect = e.get_rect(center=(x, y))
            SCREEN.blit(e, e_rect)
            x += 45


    elif level == 3: 
    ### function that blits 'subordinate clause' in dothraki
        x = 175
        y = 500

        for e in subordinate_text:
            e_rect = e.get_rect(center=(x, y))
            SCREEN.blit(e, e_rect)
            x += 45

        x = 275
        y = 550

        for e in clause_text:
            e_rect = e.get_rect(center=(x, y))
            SCREEN.blit(e, e_rect)
            x += 50

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/



pygame.init()
SCREEN = pygame.display.set_mode((800,800)) # define game screen dimensions
pygame.display.set_caption("Linguistic Gaming with Python: Lettie and Lorenzo's project") # title to be decided
clock = pygame.time.Clock()
corpus_font = pygame.font.Font('games/lettie_lorenzo/graphics/font/Grand9K_Pixel.ttf',20)
title_font = pygame.font.Font('games/lettie_lorenzo/graphics/font/Grand9K_Pixel.ttf',25)
dictionary_font = pygame.font.Font('games/lettie_lorenzo/graphics/font/Grand9K_Pixel.ttf',40)

### IN-GAME VARIABLES

game_active = False # to go to end screen
game_start = True # go to character selection screen
minigame_active = False # to minigame screen
show_dictionary_screen = False # shows dictionary object either on floor or inventory
show_dict_message = False # shows instructions once the dictionary is colleted: updated as True the first time the dictionary is collected
talk_to_npc = False # true when user initiates conversation with npc
inventory=[] # initiated as empty and then updated with 'dictionary' once collected
player=[] # initiated as empty and then updated after player character choice
instruction_count = 0 # initiated as 0 to go through instructions before the minigame starts
show_win_message = False

### BACKGROUND

background_surface = pygame.image.load('games/lettie_lorenzo/graphics/map.png').convert()
# map boundaries created with rectangles
# movement of player will be always checked for collisions against boundaries rectangles
border_rects = [
    pygame.Rect(0, 0, 800, 90),
    pygame.Rect(0, 0, 180, 200),
    pygame.Rect(0, 0, 70, 800),
    pygame.Rect(70, 620, 730, 180),
    pygame.Rect(138, 585, 730, 180),
    pygame.Rect(169, 545, 730, 180),
    pygame.Rect(465, 0, 500, 197),
    pygame.Rect(502, 0, 500, 395),
    pygame.Rect(619, 0, 500, 558),
    pygame.Rect(0, 353, 148, 80),
]
# area in which the player needs to be in order to start conversation with npc
conversation_rect = pygame.Rect(255,100,140,80)


### TEXT

# game_over screen
game_over_text = title_font.render("Game Over",False,"White")
game_over_text = pygame.transform.scale2x(game_over_text)
game_over_text_rect = game_over_text.get_rect(center = (400,350))
continue_text = corpus_font.render("press 'SPACE' to start again.",False,"White")
continue_text_rect = continue_text.get_rect(center = (400,450))

# intro_screen: character choice
intro_text1 = title_font.render("CHOOSE YOUR CHARACTER:",False,"White")
intro_text1 = pygame.transform.scale2x(intro_text1)
intro_text1_rec = intro_text1.get_rect(center = (400,250))
intro_textF = corpus_font.render("a friendly lass",False,"Black")
intro_textF_rec = intro_textF.get_rect(center = (220,400))
intro_textF1 = corpus_font.render("with a ton of hair",False,"Black")
intro_textF1_rec = intro_textF1.get_rect(center = (220,430))
intro_textM = corpus_font.render("a bald lad with",False,"Black")
intro_textM_rec = intro_textM.get_rect(center = (570,400))
intro_textM1 = corpus_font.render("a cool mustache",False,"Black")
intro_textM1_rec = intro_textM1.get_rect(center = (570,430))
instruction_text = corpus_font.render("to move in game use arrows or WASD keys",False,"White")
instruction_text_rect = instruction_text.get_rect(center = (400,600))

# dictionary screen
continue_text1 = corpus_font.render("press 'q' to exit",False,"Black")
continue_text1_rect = continue_text1.get_rect(center = (640,690))
continue_text2 = corpus_font.render("dictionary view.",False,"Black")
continue_text2_rect = continue_text2.get_rect(center = (640,730))

# above lines
# dictionary instructions
open_dictionary_text = corpus_font.render("press on dictionary to open.",False,"White")
open_dictionary_text_rect = open_dictionary_text.get_rect(center = (400,30))
# conversation instructions
start_conversation_text = corpus_font.render("press on cloud to start conversation.",False,"White")
start_conversation_text_rect = start_conversation_text.get_rect(center = (400,30))
# conversation without dictionary
conversation_0 = corpus_font.render("'Hey! Look at what is there. Come back after collecting it.'",False,"White")
conversation_0_rect = conversation_0.get_rect(center = (400,30))
conversation_1 = 0
# pre-game instrutions
pregame_instruction = ["It looks like you have everything you need now.",
                       "Before I let you pass, you must master the Dothraki language.",
                       "You shall prove that you understand Dothraki word order!",
                       "I have a scroll for you,",
                       "decipher what is written on the bottom",
                       "and select the three correct letters from the top.",
                       "If you are ready, let us begin."]
win_text = corpus_font.render("Congratulations, you learned Dothraki word order!",False,"White")
win_text_rect = win_text.get_rect(center = (400,30))

#hint text
hint_text_1 = corpus_font.render("We are Dothraki not barbarians", False, "Black")
hint_text_1_rect = hint_text_1.get_rect(center = (400, 70))
hint_text_2 = corpus_font.render("V = verb, O = object, S = ?...", False, "Black")
hint_text_2_rect = hint_text_1.get_rect(center = (400, 100))

### MUSIC

music_1 = pygame.mixer.Sound('games/lettie_lorenzo/graphics/music/Medieval_Lofi_Music_Lofi_Tavern.mp3')
music_1.set_volume(0.5) # value from 0 to 1
music_1.play(loops = -1)

### NPC

npc_surf_idle0 = pygame.image.load('games/lettie_lorenzo/graphics/player/NPC-dothraki_idle0.png').convert_alpha()
npc_surf_idle1 = pygame.image.load('games/lettie_lorenzo/graphics/player/NPC-dothraki_idle1.png').convert_alpha()
npc_surf_idle2 = pygame.image.load('games/lettie_lorenzo/graphics/player/NPC-dothraki_idle2.png').convert_alpha()
npc_surf_idle3 = pygame.image.load('games/lettie_lorenzo/graphics/player/NPC-dothraki_idle3.png').convert_alpha()
npc_surf_idle0 = pygame.transform.scale(npc_surf_idle0,(16*4,16*4))
npc_surf_idle1 = pygame.transform.scale(npc_surf_idle1,(16*4,16*4))
npc_surf_idle2 = pygame.transform.scale(npc_surf_idle2,(16*4,16*4))
npc_surf_idle3 = pygame.transform.scale(npc_surf_idle3,(16*4,16*4))

# npc only has idle animations (also when it walks, idle animations are fine as it is not noticeable for short length)
# npc working is same as player:
# the structure of lists inside list is kept as player even though not necessary because if one decided to add running animations implementation would be easier
npc = [[npc_surf_idle0,npc_surf_idle1,npc_surf_idle2,npc_surf_idle3]] # list of states: npc[0]==idle animations
npc_action = 0 # state of npc: idle or run
npc_index = 0 # animation to be selected in the state
npc_surface = npc[npc_action][npc_index]

npc_surf_rect = npc_surface.get_rect(midtop = (320,100))

# npc_move is True only in the winning condition
# target: the x point in which the NPC will move
# step: the pixels per frame for the NPC to reach the target
npc_move = False
target = 400
step = 4
npc_orientation = "Right"


### OBJECTS

# dictionary
dictionary_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dictionary.png').convert_alpha()
dictionary_surf = pygame.transform.scale(dictionary_surf,(16*3,16*3))
dictionary_rect = dictionary_surf.get_rect(center = (150,300))

# character choice scrolls
character_scroll = pygame.image.load('games/lettie_lorenzo/graphics/objects/character_scroll.png').convert_alpha()
character_scroll = pygame.transform.scale(character_scroll,(48*7,48*7))
character_scroll_rectF = character_scroll.get_rect(center = (220,420))
character_scroll_rectM = character_scroll.get_rect(center = (580,420))

# possible dialogue cloud
dialogue_cloud = pygame.image.load('games/lettie_lorenzo/graphics/objects/dialogue_cloud.png').convert_alpha()
dialogue_cloud = pygame.transform.scale(dialogue_cloud,(32*2,32*2))
dialogue_cloud_rect = dialogue_cloud.get_rect(midbottom = (345,110))


### DICTIONARY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Lettie
# Screen
dict_surf = pygame.image.load('games/lettie_lorenzo/graphics/dictionary_bg.tiff').convert_alpha()

#Letter surfaces
a_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-a.png').convert_alpha()
a_surf = pygame.transform.scale(a_surf, (16*4, 16*4))
b_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-b.png').convert_alpha()
b_surf = pygame.transform.scale(b_surf, (16*4, 16*4))
ch_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-ch.png').convert_alpha()
ch_surf = pygame.transform.scale(ch_surf, (16*4, 16*4))
d_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-d.png').convert_alpha()
d_surf = pygame.transform.scale(d_surf, (16*4, 16*4))
e_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-e.png').convert_alpha()
e_surf = pygame.transform.scale(e_surf, (16*4, 16*4))
f_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-f.png').convert_alpha()
f_surf = pygame.transform.scale(f_surf, (16*4, 16*4))
g_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-g.png').convert_alpha()
g_surf = pygame.transform.scale(g_surf, (16*4, 16*4))
h_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-h.png').convert_alpha()
h_surf = pygame.transform.scale(h_surf, (16*4, 16*4))
i_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-i.png').convert_alpha()
i_surf = pygame.transform.scale(i_surf, (16*4, 16*4))
j_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-j.png').convert_alpha()
j_surf = pygame.transform.scale(j_surf, (16*4, 16*4))
k_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-k.png').convert_alpha()
k_surf = pygame.transform.scale(k_surf, (16*4, 16*4))
kh_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-kh.png').convert_alpha()
kh_surf = pygame.transform.scale(kh_surf, (16*4, 16*4))
l_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-l.png').convert_alpha()
l_surf = pygame.transform.scale(l_surf, (16*4, 16*4))
m_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-m.png').convert_alpha()
m_surf = pygame.transform.scale(m_surf, (16*4, 16*4))
n_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-n.png').convert_alpha()
n_surf = pygame.transform.scale(n_surf, (16*4, 16*4))
o_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-o.png').convert_alpha()
o_surf = pygame.transform.scale(o_surf, (16*4, 16*4))
p_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-p.png').convert_alpha()
p_surf = pygame.transform.scale(p_surf, (16*4, 16*4))
q_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-q.png').convert_alpha()
q_surf = pygame.transform.scale(q_surf, (16*4, 16*4))
r_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-r.png').convert_alpha()
r_surf = pygame.transform.scale(r_surf, (16*4, 16*4))
s_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-s.png').convert_alpha()
s_surf = pygame.transform.scale(s_surf, (16*4, 16*4))
sh_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-sh.png').convert_alpha()
sh_surf = pygame.transform.scale(sh_surf, (16*4, 16*4))
t_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-t.png').convert_alpha()
t_surf = pygame.transform.scale(t_surf, (16*4, 16*4))
th_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-th.png').convert_alpha()
th_surf = pygame.transform.scale(th_surf, (16*4, 16*4))
v_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-v.png').convert_alpha()
v_surf = pygame.transform.scale(v_surf, (16*4, 16*4))
w_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-w.png').convert_alpha()
w_surf = pygame.transform.scale(w_surf, (16*4, 16*4))
y_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-y.png').convert_alpha()
y_surf = pygame.transform.scale(y_surf, (16*4, 16*4))
z_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-z.png').convert_alpha()
z_surf = pygame.transform.scale(z_surf, (16*4, 16*4))
zh_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/dothraki_letters/dothraki_letter-zh.png').convert_alpha()
zh_surf = pygame.transform.scale(zh_surf, (16*4, 16*4))

letters = (
    (a_surf, 'a'), (b_surf, 'b'), (ch_surf, 'ch'), (d_surf, 'd'), (e_surf, 'e'),
    (f_surf, 'f'), (g_surf, 'g'), (h_surf, 'h'), (i_surf, 'i'), (j_surf, 'j'),
    (k_surf, 'k'), (kh_surf, 'kh'), (l_surf, 'l'), (m_surf, 'm'), (n_surf, 'n'),
    (o_surf, 'o'), (p_surf, 'p'), (q_surf, 'q'), (r_surf, 'r'), (s_surf, 's'),
    (sh_surf, 'sh'), (t_surf, 't'), (th_surf, 'th'), (v_surf, 'v'), (w_surf, 'w'),
    (y_surf, 'y'), (z_surf, 'z'), (zh_surf, 'zh')
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/

### MINIGAME /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Lettie
# Screen
scroll_surf = pygame.image.load('games/lettie_lorenzo/graphics/objects/scroll_2.png').convert_alpha()
check_text = corpus_font.render("press here to check",False,"Black")
check_text_rect = check_text.get_rect(center = (425,700))

# Boxes for the characters
box = pygame.Surface((90,90))
box_rect_1 = box.get_rect(center = (275,400))
box_rect_2 = box.get_rect(center = (400,400))
box_rect_3 = box.get_rect(center = (525,400))

# Level text
clause_text = (k_surf, l_surf, a_surf, w_surf, s_surf, e_surf)
main_text = (m_surf, a_surf, i_surf, n_surf)
question_text = (q_surf, e_surf, s_surf, t_surf, i_surf, o_surf, n_surf)
subordinate_text = (s_surf, o_surf, b_surf, o_surf, r_surf, d_surf, i_surf, n_surf, a_surf, t_surf, e_surf)

# Letter lists
INCORRECT_LETTERS = [a_surf, b_surf, ch_surf, d_surf, e_surf, f_surf, g_surf, h_surf, i_surf, j_surf, k_surf, kh_surf, l_surf, m_surf, n_surf, p_surf, q_surf, r_surf, sh_surf, t_surf, th_surf, w_surf, y_surf, z_surf, zh_surf] # LOR: changed to list
ANSWER_1 = [s_surf, v_surf, o_surf]
ANSWER_2 = [v_surf, s_surf, o_surf]
ANSWER_3 = [s_surf, v_surf, o_surf]

check_answer = False
guess = [] # the player's guess gets added to this
level = 1
attempts = 0
reset()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/


### GAME LOOP ----------------------------------------------------------------------------------------------------------

while True:
    

    ### ACTIONS ----------------------------------------------------------------------------------------------
    # in this for_loop user input is checked for

    # exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if gameData["earnedPoints"] >= gameData["neededPoints"]:
                gameData["rewardText"] = "You learned the Dothraki word order!"
            GameDataLink.send_data(gameData)
            pygame.quit()
            exit()


        ## actions checked in game_active
        if game_active:

            # check positions in the screen: mouse click prints the coordinates of the clicked point
            # useful for checking positions in the map when blitting objects and creating rectangles
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos)



            if event.type == pygame.MOUSEBUTTONDOWN:

                # activate dictionary view (only if dictinary was already collected)
                # open dictionary view if collision between mouse press and dictionary rectangle is detected
                if dictionary_rect.collidepoint(event.pos) and "dictionary" in inventory:
                    show_dictionary_screen = True

                # start conversation with npc by clicking on dialogue cloud
                if dialogue_cloud_rect.collidepoint(event.pos) and start_conversation:
                    talk_to_npc = True
                else: talk_to_npc = False
                # click on dialogue cloud to proceed in the dialogue
                if dialogue_cloud_rect.collidepoint(event.pos) and dialogue_cloud_rect.bottom<100:
                    if instruction_count <= len(pregame_instruction): instruction_count+=1 # check whether dialogue texts are finished 
                    



            ## actions checked in dictionary view
            if show_dictionary_screen:

                # exit dictionary view by pressing 'q'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    show_dictionary_screen = False
                    show_dict_message = False # set to False so that next times instruction won't be shown
                    


            ## actions checked in minigame view
            if minigame_active:

                if event.type == pygame.KEYDOWN:

                    # exit minigame screen by pressing 'p'
                    if  event.key == pygame.K_p:
                        minigame_active = False

                #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Lettie
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if you click on the letter it gets put in the correct box, and added to your 'guess'
                    # if you click on the check answer button, sets check_answer to true
                    for letter in displayed_letters:
                        if letter[1].collidepoint(event.pos):
                            guess.append(letter[0])
                            if len(guess) == 1:
                                letter[1].center = (275,400)
                            elif len(guess) == 2:
                                letter[1].center = (400,400)
                            elif len(guess) == 3:
                                letter[1].center = (525,400)
                        if check_text_rect.collidepoint(event.pos):
                            check_answer = True
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/


        # actions checked in game_over game_start screen
        else:
            ## game_start screen
            if game_start:
                # choose character: by mouse press input on a rectangle: one rect for female character, one rect for male character
                # the argument passed to player_choice() is the type of character chosen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if character_scroll_rectF.collidepoint(event.pos):
                        player_choice("F")
                    elif character_scroll_rectM.collidepoint(event.pos):
                        player_choice("M")

                    # after character is loaded, player variables are set
                    player_action = 0 # set to 0 becuse idle
                    player_index = 0 # set to 0 becasuse first animation in list

                    # initial orientation is set to right because of imported image orientation
                    # if the player walks left, then a mirrored image is given as surface in .blit
                    player_orientation = "Right"

                    # player surface is taken from the list player[][], the two arguments specify what the character is doing and what animation is to be chosen
                    player_surf = player[player_action][player_index]
                    player_rect = player_surf.get_rect(center = (400,400))

                    game_start = False


            ## game_over screen
            else:
                # exit from game over screen: variables are reset and game_start is set to True to go back to character choice
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_rect.center = (400,400) # reposition player
                    npc_surf_rect.midtop = (320,100) # reposition npc
                    dialogue_cloud_rect.midbottom = (345,110) # reposition cloud
                    instruction_count = 0
                    npc_orientation = "Left"
                    
                    level = 1 
                    reset()
                    
                    game_active = False
                    game_start = True
                    inventory = [] # empty inventory
                    show_win_message = False


    ### DISPLAY ----------------------------------------------------------------------------------------------
    # here, different if statements check for different active screen blitting different things
    # minor screens are put on top for reasons of fore- and background blitting (eg dictionary screen should be accessible from minigame screen)

    ## dictionary screen
    # must be on top of minigame screen to switch back and forth while solving the puzzle
    if show_dictionary_screen:

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Lettie
        call_dictionary()
        SCREEN.blit(continue_text1,continue_text1_rect)
        SCREEN.blit(continue_text2,continue_text2_rect)

    ## minigame screen
    elif minigame_active:
        call_minigame()
        if "dictionary" in inventory:
            show_dict()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/

    ## main game screen
    elif game_active:

        SCREEN.blit(background_surface,(0,0)) # background
        # these two lines, if commented in, show the map boundaries: rectangles with red borders
        #for rect in border_rects:
            #pygame.draw.rect(SCREEN, (255, 0, 0), rect, 2)

        # next line, if commented in, shows the area in which the player should be in order for conversation cloud to pop up: rectanlge with green borders
        #pygame.draw.rect(SCREEN,(0,255,0),conversation_rect,2)


        # blit player in two scenarios:
        #   facing right: default imported images
        #   facing left: .flip(imported images)
        if player_orientation == "Right": SCREEN.blit(player_surf,player_rect)
        elif player_orientation == "Left": SCREEN.blit(pygame.transform.flip(player_surf,True,False),player_rect)
        player_animation() # animate character
        player_move() # get movement from user input

        # blit npc
        # orientation of npc depends on the position of the player on the screen: simulates npc following player
        if npc_surf_rect.colliderect(conversation_rect):
            if player_rect.x > 290: npc_orientation = "Right"
            else: npc_orientation = "Left"
        # blit different images depending on orientation
        # when npc_move==True orientation must be in the direction of walking (aka 'Right')
        if npc_move == True or npc_orientation == "Right": SCREEN.blit(npc_surface,npc_surf_rect)
        elif npc_orientation == "Left": SCREEN.blit(pygame.transform.flip(npc_surface,True,False),npc_surf_rect) # npc facing opposite direction as imported image
        npc_animation()

        # checking for collision with npc: npc works as a barrier to the victory condition
        # if a collision between player and npc is detected, player is moved away from the point of collision (simulating a wall)
        if player_rect.colliderect(npc_surf_rect):
            if player_rect.left >= npc_surf_rect.left: player_rect.left+=5
            if player_rect.right <= npc_surf_rect.right: player_rect.right-=5
            if player_rect.top <= npc_surf_rect.bottom: player_rect.top+=5
        # blit cloud only if player is in the conversation rectangle, and npc is in conversation rectangle, and npc is not moving, and dictionary instructions are not displayed
        if player_rect.colliderect(conversation_rect) and npc_surf_rect.colliderect(conversation_rect) and npc_move==False and show_dict_message==False:
            SCREEN.blit(dialogue_cloud,dialogue_cloud_rect)
            start_conversation = True # if True clicking on cloud rect can starts conversation
            talk() # checks for mouse collision with cloud: blits either conversation message or conversation instructions
        else: start_conversation = False


        show_dict() # show dictionary either on floor or inventory

        # look for collision between player and dictionary: if collision add dictionary to inventory
        if player_rect.colliderect(dictionary_rect):
            inventory.append("dictionary")
            show_dict_message = True # show instruction as True only first time collecting with dictionary


        keys = pygame.key.get_pressed()

        # winning condition: npc moves out of the way to let the player pass
        if npc_move == True:
            show_win_message = True
            win()
        if show_win_message==True:
            SCREEN.blit(win_text,win_text_rect)

        # winning condition that brings to exit screen
        # if player finds themselves in between certain values (where door is)
        if 80 <= player_rect.top <= 100 and 280 <= player_rect.left <= 350:
            game_active = False


    ## game start and game over screens
    else:
        if game_start:
            SCREEN.fill((50,70,30))
            SCREEN.blit(character_scroll,character_scroll_rectF) # player choice
            SCREEN.blit(character_scroll,character_scroll_rectM) # player choice
            SCREEN.blit(intro_text1,intro_text1_rec)
            SCREEN.blit(intro_textF,intro_textF_rec)
            SCREEN.blit(intro_textF1,intro_textF1_rec)
            SCREEN.blit(intro_textM,intro_textM_rec)
            SCREEN.blit(intro_textM1,intro_textM1_rec)
            SCREEN.blit(instruction_text,instruction_text_rect)
        else: # game_over screen		

            SCREEN.fill((50,70,30))

            player_rect.center = (350,280)
            npc_surf_rect.center = (450,280)

            SCREEN.blit(player_surf,player_rect)
            SCREEN.blit(npc_surface,npc_surf_rect)
            player_animation()
            npc_animation()

            SCREEN.blit(game_over_text,game_over_text_rect)
            SCREEN.blit(continue_text,continue_text_rect)

    # comment in the next two lines for debugging: insert variables to be tracked in curly brackets
    #debug_text = corpus_font.render(f"var1: {None}, var2: {None}, var3: {None}, var4: {None}", True, (255, 0, 0))
    #SCREEN.blit(debug_text, (10, 700))


    pygame.display.update()
    clock.tick(60)