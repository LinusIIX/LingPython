## This file includes instructions on how to start the game, what to do and contributer credits.

### 1. How to run the game:
1. Make sure a recent `Python` version is installed (tested on version 3.12.3). If you are unsure run `python --version` in a terminal (like cmd, powershell or git bash) to see your installed version of Python and update it if necessary.

2. Make sure a recent version of `pygame` is installed (tested on version 2.5.2 and 2.6.1). If you are unsure run `pip show pygame` in a terminal to see your installed version of pygame. If it is not installed or outdated, you can install it via `pip install pygame`.

3. **Make sure a recent version of `pygame-ce` is installed** (tested on version 2.5.3, every version from 2.2.0 upwards should work). If you are unsure run `pip show pygame-ce` in a terminal to see your installed version of pygame-ce. If it is not installed (most likely) or outdated, you can install it via `pip install pygame-ce`. **This is crucial, since we use pygame functions that are not part of the default pygame library!**

4. **Make sure a recent version of `requests` is installed** (tested on version 2.32.3). If you are unsure run `pip show requests` in a terminal to see your installed version of requests. If it is not installed (most likely) or outdated, you can install it via `pip install requests`. **This is crucial, since we get a default list of words from the MIT website which requires a webrequest!**

5. For all tests we used an up to date Windows 11 build. We are pretty sure, our code works operating system independant, but we sadly cannot guarantee it, since we had no device to test it on.

### 2. Game Guide
Our game is a combination of a tower defense and a typeracer game. This means that you try to type in spawning words as quickly as possible to destroy them before they reach your character and kill you.\
We build 3 gamemodes: Endless, Roguelike and Sandbox

#### 2.1 Gamemodes
1. Endless: Words spawn continuously until you die. With each kill you get, the spawn intervals get shorter, meaning more enemies spawn as the game goes on. Your goal is to get a score of 50 before you die to unlock the Dothraki hint.

2. Roguelike: Words spawn in waves, starting at 10 enemies on wave 1 and 2 more for each following round. At the end of each round you get to choose between 3 out of 9 possible upgrades (like HP or shorter enemies). Similar to the Endless mode, enemies spawn quicker as the game goes on. Your goal is to get a score of 100 before you die. **We highly recommend you trying this mode. It is a lot of fun shooting for highscores and we put a lot of affort into it.** Since the enemies spawn in waves, it is generally easier to get the required points here than the Endless mode.

3. Sandbox: Words spawn continuously but you can't die. The game ends when you choose to stop playing. You also get free access to all relevant upgrades, so you can freely choose how to play the game in this mode. The point requirement of 200 to unlock the Dothraki hint is meant for those who aren't able to achieve the required points in one of the other modes.

#### 2.2 Additional information
From the main menu you have the option to upload your own wordlists, change the starting difficulty and change the sfx volume of the game. This way, if you want to use different words than the default, **unfiltered** list from MIT, you can do so. Since pygame has its problems with special characters, we chose to filter out Umlaute (öäü) and other special characters (ß and '). For simplicity, we also chose to ignore capatilized words, just type everything in lower case and you should be fine.

Press the `esc` key to pause the game during one of the modes or quit the game from the main menu.

One fun thing we chose to do is typing support for relevant buttons. While buttons still support clicking them, most of them (marked in gray instead of black letters) also support typing out the name of the button and pressing enter to activate it. So everything (except changing sliders) can be done completely without the mouse.

### 3. Credits
We worked together on the most vital features, like the general spawning and shooting features, since they are part of every gamemode.

**Max** then transformed the base game into the roguelike mode, adding the upgrade system and wave-based spawning. He also was in charge of building the main menu, the highscore tracking across game restarts, initial button implementations and major bugfixing.

**Nikolas** transformed the base game into the sandbox mode, adding the free upgrade options. He also was in charge of loading custom wordlists into the game, giving out game sounds, refactoring all our code and planning the tasks to keep a steady pace throughout developement.

**Eilo** transformed the base game into the endless mode, adding the initial score tracking feature used in every mode. They also were in charge of integrating the game into the given GameEngine framework, returning the Dothraki hint on reached highscores, custom artworks and testing.

### 4. Information for group 14 (and potentially Prof. Butt and Mr. Sak)
Line 79 in GameEngineInterface/assets/Engine.py was changed to find the games folder, no matter from where you start the main.py file. Everything else was left untouched from our side. This change is technically not necessary but removes the need to explicitely start the game from the GameEngineInterface.
We built our game in a way, where it works in the framework but also as a standalone without printing the Dothraki hints. We originally did this to distribute the game to friends for playtesting. Since most of them have nothing to do with programming, we wanted to compact the python files into .exe files with PyInstaller. Executing .exe files messes a lot with active directories and source paths, so some special code to take that into account was necessary (as can be seen in the resource_path() function in resources.py).