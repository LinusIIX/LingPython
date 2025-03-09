import pygame
import os
from assets import Node, Engine, AnimatedSprite, globals  # Ensure this import is correct
#Class that does everything with Player
#Written in equal parts by Linus and Luca
class Player(Node):
    def __init__(self, handlesEvents, nodeRefs={}):
        super().__init__(handlesEvents, nodeRefs)
        BASE_DIR = os.getcwd()
        self.position = (0, 0)
        self.playPos = (0, 0)
        self.moveInput = [False, False, False, False]
        self.SPEED = 2.5
        self.holding = "nothing" #Important for certain interactions
        sprite_sheet = pygame.image.load(os.path.join(BASE_DIR, "assets", "ling_girl.png"))
        frames = Engine.load_sprite_sheet(sprite_sheet, 16, 16, 16)  #16px16p sprites, 16-frame animation
        self.sprite = AnimatedSprite.AnimatedSprite(frames, 100, 100) ##Anim import for pygame extended class wired
        self.sprite.animation_region = {"down":[0,3],"up":[4,7],"right":[8,11],"left":[12,15]}#The "regions" in the spritesheet where the named animation is
        self.offsetPos = (400 -48, 400 -48) # Is center - (0.5 * sprite_size * game_size) so that the player is in the center
        self.sprite_rect = self.sprite.image.get_rect()

    def process(self, dp):
        if globals.debug:
            pass
            #print(self.holding)
        hori = self.moveInput[0] - self.moveInput[2] #gets horizontal movement
        vert = self.moveInput[1] - self.moveInput[3] #gets vertical movement
        walkable = True #Helper variable to check if place is walkable bevore going there
        for collider in (self.nodeRefs["bg"].children):
            if globals.debug:
                pygame.draw.rect(dp, "blue", ((collider.getX(), collider.getY()), collider.rect_size), 15)
                pygame.draw.rect(dp, "green", ((collider.getX() + vert * self.SPEED ,collider.getY() + hori * self.SPEED), collider.rect_size), 15)
            #checks if target position is walkable
            if Engine.check_collision((collider.getX() + vert * self.SPEED ,collider.getY() + hori * self.SPEED), collider.rect_size, self) and (not collider.interactable):
                walkable = False
        if(walkable):# if the target is walkable move the background, else do nothing
            self.playPos = (self.playPos[0] + vert * self.SPEED, self.playPos[1] + hori * self.SPEED)
            self.nodeRefs["root"].setPos(self.playPos[0], self.playPos[1])

        #Just chooses the right animation
        if (hori > 0):
            self.sprite.update(self.sprite.animation_region["up"])
        elif(hori < 0):
            self.sprite.update(self.sprite.animation_region["down"])
        elif(vert > 0):
            self.sprite.update(self.sprite.animation_region["left"])
        elif(vert < 0):
            self.sprite.update(self.sprite.animation_region["right"])
        else:
            self.sprite.reset()
        #texty is the textbox that shows what you are holding(gets updated in interactable)
        texty =(pygame.font.Font('freesansbold.ttf', 32)).render(("holding: " + self.holding).upper(), True, (240, 240, 255), (50, 50, 0))
        textRect = pygame.Rect(400 - len(("holding: " + self.holding).upper()) * globals.game_size * 1.45, 50, 800, len(("holding: " + self.holding).upper()) * globals.game_size * 1.45)
        dp.blit(texty, textRect)
        dp.blit(self.sprite.image, (self.offsetPos[0], self.offsetPos[1]))

    def on_event(self, e, engine):
        if e.type == pygame.KEYDOWN:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = True #sets the corresponding input direction to true
                i += 1
        if e.type == pygame.KEYUP:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = False
                i += 1
            if e.key == pygame.K_e:
                engine.interact(self) #calls the interact function in engine checking