# contributors:
# Nikolas (refactoring)
# Eilo (framework integration)

import os
import resources

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
from menu import Menu

def main():
    try: # check if all packages are installed correctly
        # box_blur is a function exclusive to the pygame-ce extension and won't load if only pygame is installed
        from pygame.transform import box_blur
        # requests is needed to get the default word list from the web
        import requests
    except:
        try: # check if the gamedata must be returned on "error: missing package"
            from assets import GameDataLink
            GameDataLink.send_data({"Error": "For this game 'pygame-ce' and 'requests' are required but weren't found. Refer to the read.me file for instructions."})
        except:
            print("For this game 'pygame-ce' and 'requests' are required but weren't found. Refer to the read.me file for instructions.")
        finally:
            return

    pg.init()
    pg.mixer.init()
    pg.font.init()

    resources.load_assets()

    try: # check if gamedata must be tracked
        from assets import GameDataLink
        gameData = GameDataLink.get_data()
        gameData["neededPoints"] = 100
        gameData["text"] = "You need to achieve 50pts in Endless, 100pts in Roguelike or 200pts in Sandbox."
    except:
        gameData = {"earnedPoints": 0}

    game = Menu(gameData)
    game.run()

    try:
        if gameData["earnedPoints"] >= gameData["neededPoints"]:
            gameData["rewardText"] = "The allative describes a movement towards something or specifies a recipient of something. In Dothraki it is used after allative-indicating verbs like 'azhat' and formed by adding '-an' to the end of the following noun. The accusative describes the object of the sentence. In Dothraki it is used the same as in english and formed without modifications."
        GameDataLink.send_data(gameData)
    except: pass

if __name__ == '__main__':
    main()