import pygame
from pygame.locals import *
from assets import GameDataLink

gameData = GameDataLink.get_data()
gameData["neededPoints"] = 7
gameData["text"] = "in this game you have to close the window 7 times"
print(gameData)

pygame.init()
dp = pygame.display.set_mode((500, 500), pygame.HWSURFACE | pygame.DOUBLEBUF)

font = pygame.font.Font('freesansbold.ttf', 128)
text = font.render(str(gameData["earnedPoints"]), True, (0, 255, 255), (0, 0, 255))
textRect = text.get_rect()


while True:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      gameData["earnedPoints"] += 1
      if gameData["earnedPoints"] >= gameData["neededPoints"]:
        gameData["rewardText"] = "thanks for closing the windows"
      GameDataLink.send_data(gameData)
      exit()
  dp.fill((200, 255, 255))
  dp.blit(text, (100, 100))
  pygame.display.flip()
