## That should your game have

 - There should be a `main.py` file
 - This file should have a `main(gameData)` function
 - where the gameData is an object with the following layout
```json
 {
   "earnedPoints" : 0
   "neededPoints" : 45
   "text" : "info about this game"
   "rewardText" : ""
 }
```

This ensures that all games can be used to solve the entire puzzle,
as a connected list of games.

## Example in python

```python

def main(gameData):
  ... running game ...
  ...
  if quit:
    gameData["earnedPoints"] += 1
    return gameData

```



Butt send:
html
bucket, butt 

