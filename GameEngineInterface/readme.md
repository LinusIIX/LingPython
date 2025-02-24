## Integration of you game
 - ✅ There should be a `main.py` file
 - ✅ the `from assets import GameDataLink` line should be included
 - ✅ with that gameData can be acceded with:
   - `gameData = GameDataLink.get_data()` and - `GameDataLink.send_data(gameData)`
 - ✅ Your project should be independent from your device (we should try to avoid "it works on my laptop"). So we recommend before trying integration putting your project folder into another place or on another device.


the gameData is of the following layout :
```json
 {
   "earnedPoints" : 0,
   "neededPoints" : 45,
   "text" : "info about this game",
   "rewardText" : ""
 }
```

With this all games can be integrated better and make the game easier to play.
In short when testing your game put it into the games folder in the GameEngineInterface project and execute the root main.py file (details below).

- ⚠️ IMPORTANT don't change the `assets/` folder, you only have to add your project folder and execute the `main.py` file.
- ⚠️ IMPORTANT as we had some complications we use the terminal to send/receive the data this means an identifier was used to get the data so don't use `<<` and `>>` in print statements as we use them.
- ⚠️ this also means the `get_data()` function needs to be called before any print statements.
- ⚠️ Also don't use `input()` please handle inputs through pygame.
- ⚠️ IMPORTANT we have a assets module at level of your game, so no folder in your project should be ❌ `myGame/assets` ❌

## Example in python

```python
from assets import GameDataLink

gameData = GameDataLink.get_data()
gameData["neededPoints"] = 5
gameData["text"] = "This game is about this and that."
...
if exitGame:
    gameData["earnedPoints"] += 1
    GameDataLink.send_data(gameData)
    exit()
...
if doneGame:
    gameData["rewardText"] = "Well done game finished, here is a tipp / tldr what you learned"
    GameDataLink.send_data(gameData)
    exit()

```

If you have questions you can reach us through me, via e-mail `luca.pomm@uni-konstanz.de` or discord `@dezl` 🚀

Thanks for collaborating :]

When you get an error and want to write an email you can help us by giving a good context of the situation with:
- Your operating system
- The command you used to run or the full terminal output (please run in a terminal).
- Describe the file structure of the project
- You can also provide code (ideal would be your entire project so it is possible to run it)

## Hands on test in GameEngineInterface
Step by Step guid to test your project:

- First Step build your game (your project should have a `main.py` and the folder can be used to give your project a name)
- put all pictures and other assets into this folder and make sure that the paths to lode them are relative (e.g. 🚫`C:\User\Documents\OurProject\myPicture.png`, like this ✅ `/myPicture.png`)
- Now you can download the GameEngineInterface zip and unzip it, for testing
- There is a games folder put your project folder here (like `GameEngineInterface/games/myGame`)
- Now as written above or close to the examples add the GameDataLink lines of code
- Your done, now you can test your project by executing the test environment at `python3 GameEngineInterface/main.py`

Select your project name and, by moving there by w,a,s,d and starting your game with pressing e. Now you can test your game. At the end you can see in the terminal if the gameData was transmitted.