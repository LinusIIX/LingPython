## Project Integration
To make the final combined project work as intended the projects need to be integrated in some form.
For provide/require 2 different levels of integration.
1. Loos integration: <br>
 We will start your game independent from the hole game and let the player gather info on his own. We only want a return statement if the game was completed, example of this:
 ```py
 ...
 while True:
    state = myGameLoop()
    if state == "game finished":
       return True
    if state == "game close":
        return False
    ...
 ```
 2. Tight integration: <br>
 Here you need to make a new import statement to get the game and its context. With this your game module can rely on our game objects and use them and the game context to integrate the experience into the game more coherently.
 ```py
 import StoneSong
 ...
 def setup():
     ...
 def loop():
     ...
 ```