import json
import os
import pygame
from assets import Engine, Node, GameDataLink, Player, BackGround, EventStone, TextDisplay, globals, AnimatedSprite

#Written by Luca
class EndScreen(Node):
    def __init__(self, handlesEvents=False, nodeRefs=..., callProcess=True):
        super().__init__(handlesEvents, nodeRefs, callProcess)
        
        BASE_DIR = os.getcwd()
        sprite_sheet = pygame.image.load(os.path.join(BASE_DIR, "assets", "end_anim.png"))
        frames = Engine.load_sprite_sheet(sprite_sheet, 800, 800, 14, 1)  #16px16p sprites, 16-frame animation
        self.sprite = AnimatedSprite(frames, 100, 100) ##Anim import for pygame extended class wired
        self.sprite.animation_region={"base" : [0, 13]}

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.credits = open("credits.txt").read().split("\n")
        self.components = []

    def process(self, dp):
        if self.sprite.index < 13:
            self.sprite.update(self.sprite.animation_region["base"])
        dp.blit(self.sprite.image, (0, 0))
        if self.sprite.index == 13 and self.components == []:
            for idx, text in enumerate(self.credits):
                textSurface = self.font.render(text, True, (255, 255, 255), (0, 0, 0))
                textRect = pygame.Rect(400 - len(text) * globals.game_size * 1.45, 650 + idx * 50, 800, len(text) * globals.game_size * 1.45)
                self.components.append({
                    "display" : textSurface,
                    "rect" : textRect
                })
        
        for component in self.components:
            component["rect"].top -= 2
            dp.blit(component["display"], component["rect"])
            if component["rect"].top < -4000:
                exit()
        

#Written by Luca & Linus

#Initialize the Engine object
engine = Engine()
#Create a root node to attach most other object to that should move on screen
root = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
engine.add_node(root)

#Container for EventStone
eventStoneContainer = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
#Initialize Player it should handle events
player = Player(handlesEvents=True)
#Add EndScreen
endScreen = EndScreen(callProcess=False)
#Add Background with node references to other nodes to add stuff
backGround = BackGround((650, 600), nodeRefs= {
    "player" : player,
    "endScreen" : endScreen
})
eventStoneContainer.position = backGround.position
root.add_node(backGround)
root.setPos(player.position[0],player.position[1])

#load data to set EventStones
eventStoneData = json.loads(open("eventStoneData.json").read())
root.add_node(eventStoneContainer)
for data in eventStoneData:
    eventStoneContainer.add_node(EventStone(data["module"], data["description"], data["position"], data["rect_size"]))

#set nodeRefs for player
player.nodeRefs = {
    "root" : root,
    "bg"   : backGround,
}
player.rect_size = (player.sprite_rect.width,player.sprite_rect.height)
engine.add_node(player)

#ui for display of event description
playerUI = TextDisplay(handlesEvents=False, nodeRefs={"player" : player, "eventStoneContainer" : eventStoneContainer})
root.add_node(playerUI)

#last we add the endScreen on top
engine.add_node(endScreen)

#now we start pygame with run() in engine
engine.run()