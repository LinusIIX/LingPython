## Integration of you game
 - ✅ There should be a `main.py` file
 - ✅ the `from assets import GameDataLink` line should be included
 - ✅ with that gameData can be acceded with:
   - `gameData = GameDataLink.get_data()` and - `GameDataLink.send_data(gameData)`


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

- (!) IMPORTANT as we had some complications we use the terminal to send/receive the data this means an identifier was used to get the data so don't use `<<` and `>>` in print statements as we use them.

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

If you have questions you can reach us through me, via e-mail `luca.pomm@uni-konstanz.de` or discord `@dezl`

Thanks for collaborating :]

## Hands on test in GameEngineInterface
Step by Step guid to test your project:

- First Step build your game (your project should have a `main.py` and the folder can be used to give your project a name)
- Now you can download the GameEngineInterface zip and unzip it, for testing
- There is a games folder put your project folder here (like `GameEngineInterface/games/myGame`)
- Now as written above or close to the examples add the GameDataLink lines of code
- Your done, now you can test your project by executing the test environment at `python3 GameEngineInterface/main.py`

Select your project name and, by moving there by w,a,s,d and starting your game with pressing e. Now you can test your game. At the end you can see in the terminal if the gameData was transmitted.