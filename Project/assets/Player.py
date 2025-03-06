import pygame
import os
from assets import Node, globals  # Ensure this import is correct


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y, frame_rate=100):
        super().__init__()
        self.images = images  # List of frames
        self.index = 0  # Current frame index
        self.image = self.images[self.index]
        self.temp_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rate = frame_rate  # Time (ms) per frame
        self.last_update = pygame.time.get_ticks()  # Track last update time
        self.animation_region =  {"base" : [0,0]}

    def update(self,animation):
        """Cycle through frames based on time."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index = animation[0] + ((self.index + 1) % 4)  # Loop                  animation here lookie
            self.image = self.images[self.index]  # Update current frame
    def reset(self):
        self.index = 0
        self.image = self.images[self.index]
    
def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame_rect = frame.get_rect()
        frame = pygame.transform.scale(frame, (globals.game_size * frame_rect.width, globals.game_size * frame_rect.height))
        frames.append(frame)
    return frames


class Player(Node):
    def __init__(self, handlesEvents, nodeRefs):
        super().__init__(handlesEvents, nodeRefs)
        BASE_DIR = os.path.dirname(__file__)
        self.position = (0, 0)
        self.playPos = (0, 0)
        self.moveInput = [False, False, False, False]
        self.SPEED = 1.5
        sprite_sheet = pygame.image.load(os.path.join(BASE_DIR, "ling_girl.png"))
        frames = load_sprite_sheet(sprite_sheet, 16, 16, 16)  #16px16p sprites, 16-frame animation
        self.sprite = AnimatedSprite(frames, 100, 100)
        self.sprite.animation_region = {"down":[0,3],"up":[4,7],"right":[8,11],"left":[12,15]}
        self.offsetPos = (400 -48, 400 -48) # Ist center - (0.5 * sprite_size * game_size)
        self.sprite_rect = self.sprite.image.get_rect()
        #print(self.sprite.get_rect())

    def process(self, dp):
        hori = self.moveInput[0] - self.moveInput[2]
        vert = self.moveInput[1] - self.moveInput[3]
        self.playPos = (self.playPos[0] + vert * self.SPEED, self.playPos[1] + hori * self.SPEED)
        #print((self.position[0] + vert * self.SPEED, self.position[1] + hori * self.SPEED))
        self.nodeRefs["root"].setPos(self.playPos[0] + vert, self.playPos[1] + hori)
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
        dp.blit(self.sprite.image, (self.offsetPos[0], self.offsetPos[1]))
        #dp.blit(self.sprite.image, (self.offsetPos[0] - self.sprite_rect.centerx, self.offsetPos[1] - self.sprite_rect.centery))

    def on_event(self, e, engine):
        if e.type == pygame.KEYDOWN:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = True
                i += 1
        if e.type == pygame.KEYUP:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = False
                i += 1
            if e.key == pygame.K_e:
                engine.interact(self)
