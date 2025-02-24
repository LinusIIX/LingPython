import pygame
from pygame.locals import *
from assets import GameDataLink

gameData = GameDataLink.get_data()
gameData["neededPoints"] = 5
gameData["text"] = "type in all 5 words 'hello from my word checker'"

wordCheck = ["hello", "from", "my", "word", "checker"]
word = wordCheck[gameData["earnedPoints"]]

dp = pygame.display.set_mode((800, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)

while True:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      GameDataLink.send_data(gameData)
      exit()
    if e.type == pygame.KEYUP:
      if e.unicode == word[0]:
        word = word[1:]
        if len(word) == 0:
          gameData["earnedPoints"] += 1
          if gameData["earnedPoints"] >= gameData["neededPoints"]:
            gameData["rewardText"] = "well you typed like a pro :]"
          GameDataLink.send_data(gameData)
          exit()
  dp.fill((200, 200, 100))
  pygame.display.flip()
