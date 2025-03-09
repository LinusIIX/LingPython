import pygame

#Helper class to animate
#Writen by Linus
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y, frame_rate=100):
        super().__init__()
        self.images = images  # List of frames
        self.index = 0  # Current frame index
        self.image = self.images[self.index] #Current Frame
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rate = frame_rate  # Time (ms) per frame
        self.last_update = pygame.time.get_ticks()  # Track last update time
        self.animation_region =  {"base" : [0,0]} #So it doesnt crash

    def update(self,animation):
        """Cycle through frames based on time."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index = animation[0] + ((self.index + 1) % (animation[1] - animation[0] + 1))  # Loop                  animation here lookie
            self.image = self.images[self.index]  # Update current frame
    def reset(self):
        self.index = 0
        self.image = self.images[self.index]