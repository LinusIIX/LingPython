#PROJECT: LEARN 20 DOTHRAKI VERBS
#AUTHOR: FILIPE REBELO BAIXINHO

#integration stuff

#from assets import GameDataLink

#gameData = GameDataLink.get_data()
#gameData["neededPoints"] = 5
#gameData["text"] = "This game is about this and that."

#if exitGame:
#	gameData["earnedPoints"] += 1
#	GameDataLink.send_data(gameData)
#	exit()

#if doneGame:
#	gameData["rewardText"] = "Well done game finished, here is a tipp" 
#	GameDataLink.send_data(gameData)
#	exit()

#1. INTRODUCTION
#in this first short section the hero of this game and the initial context are introduced

#throughout the whole program, the story is told using open-source ASCII art images taken
#mostly from www.asciiart.eu/

print(
r'''

                       /\
        _/\           /  \
    _  /   \         /    \/\
   / \/   _ \     /\/\  _  _/\
  /   \_ / \/\_/\/_/  \/ \/   \
 /\/\   \_   /   \/            \
/    \___/\ /     \             \
           \       \             \
           .-"---.  \             \
__..---.. /       \  \             \
         /\___.-'./\''--..____..--''	OUR HERO CONTINUES HIS QUEST!
`-.      \/ O) (O \/ ''--.._
    __    |  (_)  |         _.-'-._	HE'S WANDERING THROUGH HILLS AND VALLEYS.
   / /  __/\\___//\__ ..--''-._
   | (_/\ \/`---'\/ /\         `-._	HOPING TO GATHER SUFFICIENT CLUES
_.-\ \/  \  \   /  /  \.-'-._
   /\|   /  -| |-  \   \     `-._	TO CRACK THAT MYSTERIOUS INSCRIPTION...
  | ||  /\  -| |-  /\   \        `-.
   \/|_/ |  -|_\-  |/   /
   \ \   /  /B_B\  \\  /
   / (   \_/  _  \_/ \/
.__\ \   /    |    \_/
   ) /''-| __ | __ |
   |(    \    |    /---...___
   /|    /____|____\         '-._
   ||     |   ||   |
   \\     ///\\//\\\
jro \|   oOO(_)(_)OOo

''')

#the following print()/input()/print() chunk of code is repeated all across the program, to set storytelling frames apart
#and to allow the user to move on to the next frame at his/her own pace

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''

	 BY CHANCE (OR PERHAPS FATE) HE FINDS A CABIN
		 VERY HIGH IN THE MOUNTAINS


                                  /\
                              /\  //\\
                       /\    //\\///\\\        /\
                      //\\  ///\////\\\\  /\  //\\
         /\          /  ^ \/^ ^/^  ^  ^ \/^ \/  ^ \
        / ^\    /\  / ^   /  ^/ ^ ^ ^   ^\ ^/  ^^  \
       /^   \  / ^\/ ^ ^   ^ / ^  ^    ^  \/ ^   ^  \       *
      /  ^ ^ \/^  ^\ ^ ^ ^   ^  ^   ^   ____  ^   ^  \     /|\
     / ^ ^  ^ \ ^  _\___________________|  |_____^ ^  \   /||o\
    / ^^  ^ ^ ^\  /______________________________\ ^ ^ \ /|o|||\
   /  ^  ^^ ^ ^  /________________________________\  ^  /|||||o|\
  /^ ^  ^ ^^  ^    ||___|___||||||||||||___|__|||      /||o||||||\       |
 / ^   ^   ^    ^  ||___|___||||||||||||___|__|||          | |           |
/ ^ ^ ^  ^  ^  ^   ||||||||||||||||||||||||||||||oooooooooo| |ooooooo  |
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

#2. TRIP TO THE ORACLE
#in this second section the hero is given a dictionary which he'll be able to use later in order to win the main game

'''the following small dictionary is adapted from the dothraki dictionary
that can be found online at languagechaos.com/dothraki/dict
'''

dictionary = {
"1. ezhirat:" : "to dance",
"2. notat:":"to turn",
"3. kemat:":"to marry",
"4. addrivat:":"to kill",
"5. adakhat:":"to eat",
"6. remekat:" : "to sleep",
"7. lathat:" : "to be awake",
"8. lanat:" :"to run",
"9. laqat:" : "to cry",
"10. hoyalat:" : "to sing",
"11. ezolat:" : "to learn",
"12. dirgat:" :"to think",
"13. zerqolat:": "to swim",
"14. rhelalat:":"to help",
"15. ifat:" : "to walk",
"16. astat:" : "to say",
"17. affazhat:" : "to give warmth to",
"18. esazhalat:" : "to take something back",
"19. vineserat:": "to remember",
"20. fichat:" : "to take"
}

print(
r'''
	 IT SEEMS NO ONE IS THERE 

		 HE KNOCKS ON THE DOOR 

	 BUT TO NO AVAIL 

            __________
           |  __  __  |
           | |  ||  | |
           | |  ||  | |
           | |__||__| |
           |  __  __()|
           | |  ||  | |
           | |  ||  | |
           | |  ||  | |
           | |  ||  | |
           | |__||__| |
ejm        |__________|
''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''

	 CAREFULLY OUR HERO STEPS IN... 

		 ONLY TO FIND A VERY APPEALING BED 

     _   ()
() .'_`'.||
||/.| ||\ |
| /|| || ||         _   ()
|| || || ||    () .'_`'.||
|| || || ||    ||/.| ||\ |
|| || |I-'`-._ | /|| || ||
||_I'`_.-||-._`'| || || ||
m._ <'_  ||   `|| || || ||
i| `-._`-'|    || || |I-'|
c)     `-._`-._||_I'`_.-||
           `-._` _.-'   ()
               ||       `
               ()

	 THE BODY COULD USE SOME REST, OUR HERO THINKS 

		 SO HE LAYS DOWN HIS BURDEN AND TAKES A QUICK NAP 

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''	    zzz
	  zzz
	zzz
      _____|~~\_____      _____________
  _-~               \    |    \
  _-    | )     \    |__/   \   \
  _-         )   |   |  |     \  \
  _-    | )     /    |--|      |  |
 __-_______________ /__/_______|  |_________
(                |----         |  |
 `---------------'--\\\\      .`--'
                              `||||

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
                _                                  
              (`  ).                   _           
             (     ).              .:(`  )`. THROUGH THE LAND OF DREAMS
)           _(       '`.          :(   .    )      OUR HERO WANDERS...
        .=(`(      .   )     .--  `.  (    ) )      
       ((    (..__.:'-'   .+(   )   ` _`  ) )                 
`.     `(       ) )       (   .  )     (   )  ._   
  )      ` __.:'   )     (   (   ))     `-'.-(`  ) 
)  )  ( )       --'       `- __.'         :(      )) 
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'          
                                        
--..,___.--,--'`,---..-.--+--.,,-,,..._.--..-._.-a:f--.

''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
              .
               					
              |					
     .               /				
      \       I     				
                  /		FROM BEHIND THE CLOUDS
        \  ,g88R_	A LIGHT APPEARS
          d888(`  ).                   _	GROWING IN INTENSITY
 -  --==  888(     ).=--           .+(`  )`.
)         Y8P(       '`.          :(   .    )
        .+(`(      .   )     .--  `.  (    ) )
       ((    (..__.:'-'   .=(   )   ` _`  ) )
`.     `(       ) )       (   .  )     (   )  ._
  )      ` __.:'   )     (   (   ))     `-'.:(`  )
)  )  ( )       --'       `- __.'         :(      ))
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'
                                        	
--..,___.--,--'`,---..-.--+--.,,-,,..._.--..-._.-a:f--.
''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
          |		IT SEEMS A STAR IS MOVING TOWARDS US!
          |   .
   `.  *  |     .'
     `. ._|_* .'  .
   . * .'   `.  *
-------|     |-------
   .  *`.___.' *  .
      .'  |* `.  *
    .' *  |  . `.
        . |
          | jgs
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''

                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/
                |     |
                |     |
                |     |
                |     |
                |     |
                |     |
                |     |
                |     |
           jgs  |     |
                \_.__./

''')



print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''


                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/
                |     |		FEAR NOT, PILGRIM!
                |     |
                |     |
                |     |
                |     |
                |     |
                |     |
                |     |
           jgs  |     |
                \_.__./
''')



print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''


                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/	I AM THE ORACLE OF THE MOUNTAINS...
                |     |
                |     |
                |     |	I'VE BEEN WATCHING YOUR JOURNEY FROM AFAR
                |     |
                |     |	WITH GREAT INTEREST!
                |     |
                |     |
                |     |		I WOULD LIKE TO HELP YOU...
           jgs  |     |
                \_.__./
''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''


                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/	WHEN YOU WAKE UP
                |     |
                |     |	YOU'LL FIND A BOOK NEXT TO YOU.
                |     |
                |     |	YOU'LL WONDER IF IT'S OF ANY USE.
                |     |
                |     |	BUT ITS USE IS ONLY LATER TO REVEAL ITSELF.
                |     |
            	|     |
           jgs  |     |
                \_.__./ 
			
''')



print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''


                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/
                |     | TAKE IT WITH YOU!
                |     |
                |     | AND YOUR VENTURE SHALL REACH SUCCESS,
                |     |
                |     | FOR THE GODS ARE WITH YOU, PILGRIM.
                |     |
                |     |
            	|     |
           jgs  |     |
                \_.__./
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''


                   _
                 *"_"*
        _..._    /`_`\    _..._
      .'     '. | / \ | .'     '.
,    /         ')\^_^/('         \    ,
\`--'  .--.    (_.> <._)    .--.  '--`/
 '.__.'    '._/   \_/   \_.'    '.__.'
             /     _     \
             \  \_/|\_/  /
              \  //^\\  /
               \/`   `\/
                |     | 	GODSPEED!
                |     |
                |     | 
                |     |
                |     | 
                |     |
                |     |
            	|     |
           jgs  |     |
                \_.__./
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
		 OUR HERO WAKES UP 
			 WHAT A STRANGE DREAM, HE THINKS! 
     _   ()
() .'_`'.||
||/.| ||\ |
| /|| || ||         _   ()
|| || || ||    () .'_`'.||
|| || || ||    ||/.| ||\ |
|| || |I-'`-._ | /|| || ||
||_I'`_.-||-._`'| || || ||
m._ <'_  ||   `|| || || ||
i| `-._`-'|    || || |I-'|
c)     `-._`-._||_I'`_.-||
           `-._` _.-'   ()
               ||       `
               ()


''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
		 HE FEELS AN OBJECT NEXT TO HIM ON THE BED 
			 AND TURNS AROUND TO SEE IT 
     _   ()
() .'_`'.||
||/.| ||\ |
| /|| || ||         _   ()
|| || || ||    () .'_`'.||
|| || || ||    ||/.| ||\ |
|| || |I-'`-._ | /|| || ||
||_I'`_.-||-._`'| || || ||
m._ <'_  ||   `|| || || ||
i| `-._`-'|    || || |I-'|
c)     `-._`-._||_I'`_.-||
           `-._` _.-'   ()
               ||       `
               ()


''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
   ,   ,
  /////|
 ///// |		 WHAT BOOK IS THIS? 
|~~~|  |	 PERHAPS IT WAS NOT ALL A DREAM AFTER ALL 
|===|  |
|j  |  |
| g |  |
|  s| /
|===|/
'---'
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
    __________________   __________________
.-/|                  \ /                  |\-.
||||                   |                   ||||
||||                   |       ~~*~~       ||||
||||    --==*==--      |                   ||||		A DICTIONARY?
||||                   |                   ||||	 SO IT SEEMS...
||||                   |                   ||||	 BUT ONLY A FEW TERMS
||||                   |     --==*==--     ||||	 WERE TRANSLATED
||||                   |                   ||||	 INTO ENGLISH...
||||                   |                   ||||
||||                   |                   ||||	 LET'S TAKE A CLOSER LOOK...
||||                   |                   ||||
||||__________________ | __________________||||
||/===================\|/===================\||
`--------------------~___~-------------------''
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

#at this point the dictionary that was created earlier in the code is first displayed
#to the user. He can study it, but also just come back to it later on, once he understands
#how the dictionary can be useful to him/her

print("\n\tPERHAPS IT WILL BE USEFUL TO STUDY THIS CAREFULLY, OUR HERO THINKS...\n\n") 

#the dictionary is presented in two steps for aesthetic reasons

print("\t\tfirst page:\n")

for i in dictionary:
	if '10' in i:
		print("\t",i,dictionary[i],"\t\n")
		print("\n"*5)
		input("...	...	...")
		print("\n"*5)
		print("\t\tsecond page:\n")
	else:
		print("\t",i,dictionary[i],"\t\n")

print("\n\t...WHO KNOWS THE POWER OF THESE WORDS?\n")

print("\n"*5)
input("...	...	...")
print("\n"*5)

print("\t\t\tINTERESTING...\n")

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''		OUR HERO IS STILL TRYING TO FIGURE THE USE OF THIS NEW TOOL
			AS THE SUN IS SETTING BEYOND THE MOUNTAIN RANGE


  ........::::::::::::..           .......|...............::::::::........
     .:::::;;;;;;;;;;;:::::.... .     \   | ../....::::;;;;:::::.......
         .       ...........   / \\_   \  |  /     ......  .     ........./\
...:::../\\_  ......     ..._/'   \\\_  \###/   /\_    .../ \_.......   _//
.::::./   \\\ _   .../\    /'      \\\\#######//   \/\   //   \_   ....////
    _/      \\\\   _/ \\\ /  x       \\\\###////      \////     \__  _/////
  ./   x       \\\/     \/ x X           \//////                   \/////
 /     XxX     \\/         XxX X                                    ////   x
-----XxX-------------|-------XxX-----------*--------|---*-----|------------X--
       X        _X      *    X      **         **             x   **    *  X
      _X                    _X           x                *          x     X_
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''

                |
                |		 AFTER A NIGHT OF DREAMLESS SLEEP,
      `.        |        .'		STILL CLUELESS,
        `.    .---.    .'			OUR HERO GREETS THE MORNING SUN
           .~       ~.
          /   O   O   \			AND DESCENDS DOWN THE MOUNTAIN,
-- -- -- (             ) -- -- --	ONCE AGAIN... 
          \    `-'    /
           ~.       .~
        .'    ~---~    `.
      .'        |        `.
                |
                |
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


#3. MEET THE TROLLS
#in this third section, the main plot in our game is introduced.
#the hero meets two villains and a snail in need of rescue
#he'll be proposed to play a game (section 4) in order to save the snail

print(
r'''
                       /\
        _/\           /  \
    _  /   \         /    \/\
   / \/   _ \     /\/\  _  _/\
  /   \_ / \/\_/\/_/  \/ \/   \
 /\/\   \_   /   \/            \
/    \___/\ /     \             \
           \       \             \
           .-"---.  \             \
__..---.. /       \  \             \
         /\___.-'./\''--..____..--''	THE MOUNTAINS ARE NOW LEFT BEHIND.
`-.      \/ O) (O \/ ''--.._
    __    |  (_)  |         _.-'-._	THE JOURNEY SHALL CONTINUE.
   / /  __/\\___//\__ ..--''-._
   | (_/\ \/`---'\/ /\         `-._	DESTINATION: UNKNOWN (TO US AND THE PILGRIM ANYWAY)
_.-\ \/  \  \   /  /  \.-'-._
   /\|   /  -| |-  \   \     `-._	UPWARDS AND ONWARDS, THAT'S THE MOTTO.
  | ||  /\  -| |-  /\   \        `-.
   \/|_/ |  -|_\-  |/   /
   \ \   /  /B_B\  \\  /
   / (   \_/  _  \_/ \/
.__\ \   /    |    \_/
   ) /''-| __ | __ |
   |(    \    |    /---...___
   /|    /____|____\         '-._
   ||     |   ||   |
   \\     ///\\//\\\
jro \|   oOO(_)(_)OOo

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''

	 SUDDENLY A BRIDGE APPEARS ON THE HORIZON 

                                       ^^
    ^^      ..                                       ..
            []                                       []
          .:[]:_          ^^                       ,:[]:.
        .: :[]: :-.                             ,-: :[]: :.
      .: : :[]: : :`._                       ,.': : :[]: : :.
    .: : : :[]: : : : :-._               _,-: : : : :[]: : : :.
_..: : : : :[]: : : : : : :-._________.-: : : : : : :[]: : : : :-._
_:_:_:_:_:_:[]:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:[]:_:_:_:_:_:_
!!!!!!!!!!!![]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![]!!!!!!!!!!!!!
^^^^^^^^^^^^[]^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[]^^^^^^^^^^^^^
            []                                       []
            []                                       []
            []                                       []
 ~~^-~^_~^~/  \~^-~^~_~^-~_^~-^~_^~~-^~_~^~-~_~-^~_^/  \~^-~_~^-~~-
~ _~~- ~^-^~-^~~- ^~_^-^~~_ -~^_ -~_-~~^- _~~_~-^_ ~^-^~~-_^-~ ~^
   ~ ^- _~~_-  ~~ _ ~  ^~  - ~~^ _ -  ^~-  ~ _  ~~^  - ~_   - ~^_~
     ~-  ^_  ~^ -  ^~ _ - ~^~ _   _~^~-  _ ~~^ - _ ~ - _ ~~^ -
jgs     ~^ -_ ~^^ -_ ~ _ - _ ~^~-  _~ -_   ~- _ ~^ _ -  ~ ^-
            ~^~ - _ ^ - ~~~ _ - _ ~-^ ~ __- ~_ - ~  ~^_-
                ~ ~- ^~ -  ~^ -  ~ ^~ - ~~  ^~ - ~

		 A BRIDGE IS ALWAYS A GOOD OMEN 
''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

print("\t\tA SIGN OF HOPE...")


print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\ BUT IS IT REALLY?!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''

	HELP!
	HELP!			@             _________
 	HELP!			 \____       /         \
				 /    \     /   ____    \
				 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''

	THESE TROLLS
	HAVE TAKEN ME HOSTAGE!	@             _________
 				 \____       /         \
	PLEASE FREE ME!		 /    \     /   ____    \
				 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 HAHAHAHA! THAT WILL BE THE DAY!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')


print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 YOU KNOW WHAT?! YOU CAN TAKE HIM WITH YOU...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 THAT IS... IF YOU CAN WIN A LITTLE GAME!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 YOU SEE... WE'RE NOT JUST ANY EVIL TROLLS!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		NO, SIR!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 WE'RE NEOGRAMMARIAN TROLLS!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YES, INDEED!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 WE WERE ONCE DOING REALLY WELL!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YES! UNTIL THAT YANKEE CAME...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 YOU SEE! WE STUDIED UNDER HERR HERMANN PAUL...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		BUT THAT DAMNED CHOMSKY TOOK OUR JOBS AWAY!
|     \     \|"""",		WITH THOSE FANCY TREES...
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 BUT WE'LL GET OUR REVENGE!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		WE'LL CAPTURE EVERY LINGUIST
|     \     \|"""",		THAT IS ON A LINGUISTIC JOURNEY...
|      \     ______)		THROUGH OUR BRIDGE HAHAHA!
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 YOU LOOK LIKE A LINGUIST!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YES! LET'S PLAY A GAME!
|     \     \|"""",		IF YOU WIN, YOU TAKE THE DIRTY SNAIL WITH YOU...
|      \     ______)		IF YOU LOSE, WELL... YOU DIE HAHAHA!
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
                       /\
        _/\           /  \
    _  /   \         /    \/\
   / \/   _ \     /\/\  _  _/\
  /   \_ / \/\_/\/_/  \/ \/   \
 /\/\   \_   /   \/            \
/    \___/\ /     \             \
           \       \             \
           .-"---.  \             \
__..---.. /       \  \             \
         /\___.-'./\''--..____..--''	WELL, I'M NOT A LINGUIST...
`-.      \/ O) (O \/ ''--.._
    __    |  (_)  |         _.-'-._	BUT I HAVE A LOT OF LINGUISTIC INTUITIONS
   / /  __/\\___//\__ ..--''-._
   | (_/\ \/`---'\/ /\         `-._	THAT SHOULD SUFFICE TO SAVE THE SNAIL!
_.-\ \/  \  \   /  /  \.-'-._
   /\|   /  -| |-  \   \     `-._
  | ||  /\  -| |-  /\   \        `-.
   \/|_/ |  -|_\-  |/   /
   \ \   /  /B_B\  \\  /
   / (   \_/  _  \_/ \/
.__\ \   /    |    \_/
   ) /''-| __ | __ |
   |(    \    |    /---...___
   /|    /____|____\         '-._
   ||     |   ||   |
   \\     ///\\//\\\
jro \|   oOO(_)(_)OOo

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)



print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 HE SOUNDS LIKE HE HAS READ CHOMSKY(1957)
|     \     \|"""",		... OH THE DAMAGE OF THE GENERATIVISTS
|      \     ______)		IS NOW BEYOND THE REALM OF LINGUISTICS!
\       \  /`			IT HAS REACHED THE COMMON MAN...
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		VERY WELL, THEN! LET'S PLAY!
|     \     \|"""",		IF YOU WIN, YOU CAN TAKE THE DIRTY SNAIL WITH YOU...
|      \     ______)		IF YOU LOSE... YOU'RE OF NO USE TO US ANYWAY.
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


print(
r'''
    ___(                        )
   (                          _)
  (_                       __))
    ((                _____)
      (_________)----'
         _/  /			THE THUNDER ROARS...
        /  _/
      _/  /	AND THE GAME BEGINS!
     / __/
   _/ /
  /__/
 //
/'

''')


print("\n"*5)
input("...	...	...")
print("\n"*45)


#section 4 - quiz
#this section contains the game
#it's a simple multiple choice game
#the names of songs are translated in dothraki and the user must translate them back into english
#subsequently he must guess which of two artists recorded the given song 

#variables

	#counters
errors = 0 #set counter for mistakes
correct = 0 #set counter for correct answers

	#empty variables
choice = ""
guess = ""

	#answers
solution = "1"
wrong_answer = "2"

	#questions
question = "Which of these two artists played"
quest_ans_pairs = {
"'lanatas,lanatas,lanatas'?\n\n":"\t[1]: The Velvet Underground\n\t[2]: Chic\n",
"'dirgatas'?\n\n":"\t[1]: Curtis Mayfield \n\t[2]: Paul Robeson\n",
"'notatas!notatas!notatas!'?\n\n":"\t[1]: The Byrds \n\t[2]: The Clash\n",
"'vineseratas'?\n\n":"\t[1]: Jimi Hendrix \n\t[2]: Karl May\n",
"'rhelalatas'?\n\n":"\t[1]: The Beatles \n\t[2]: The Beach Boys\n",
}


#functions

def play(r):
	print(question)
	'''this function can be used inside a for loop of range 5
	and will iterate through all the elements in the question answer pairs
	printing them and allowing the player to choose one answer for each
		if the answer is correct, the correct counter increases
		if the answer is incorrect, the  error counter will increase
		in any other case, it will let the player know that the answer was not valid 
	'''
	#the global keys allow the function to update globally (that is, non-locally) the values of these variables
	#that's useful to make sure the if-conditions around which the function will be used work correctly
	global errors
	global correct

	#this presents a given question and allows the user to answer
	print(question,list(quest_ans_pairs)[r],list(quest_ans_pairs.values())[r])
	guess = input("\nYour guess: ")

	#correct answer
	if guess.lower() == solution:
		print(
r'''

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	YOU GOT LUCKY!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		correct += 1

	#wrong answer
	elif guess.lower() == wrong_answer:
		print(
r'''

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	HAHA! WE GOT YOU THIS TIME...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		errors += 1

	#invalid answer
	else:
		print(
r'''

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	YOU KNOW THAT'S NOT A VALID ANSWER!.
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')

		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		errors += 1

#game introduction
print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 WE'LL GIVE YOU THE NAMES OF SOME FAMOUS SONGS
|     \     \|"""",		...THESE NAMES HAVE BEEN TRANSLATED IN DOTHRAKI...
|      \     ______)		BUT IT'S NOT THAT DIFFICULT HAHAHA!
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YES! IT'S NOT THAT DIFFICULT. AFTER ALL,
|     \     \|"""",		THESE SONGS ONLY HAVE VERBS IN THEIR NAMES...
|      \     ______)
\       \  /`
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)

#game loop
while errors < 3 and choice != "0": #main loop
	'''the loop will break in 3 situations
	if the player makes 3 mistakes
	if the player chooses to quit in the entry menu
	if the player successfuly answers 3 questions out of the 5
	'''
	#options menu(quit, study or play!)
	print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 READY TO PLAY?
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

	    0 - Quit
	    1 - Check dictionary
	    2 - Play!
''')

	choice = input("Choice: ")
	print("\n"*45) #this is just a line break

	#iterate through the five question answer pairs
	for i in range(5):

		#check dictionary
		if choice == "1":
			print("\t\tfirst page:\n")
			for i in dictionary:
				if '10' in i:
					print("\t",i,dictionary[i],"\t\n")
					print("\n"*5)
					input("...	...	...")
					print("\n"*5)
					print("\t\tsecond page:\n")
				else:
					print("\t",i,dictionary[i],"\t\n")
			print("\n"*5)
			input("...	...	...")
			print("\n"*5)
			break

		#question/answer
		elif choice == "2": #the game!!
			play(i)

	if choice == "0": #quit game
		print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	COME AGAIN ANYTIME!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		WE'LL BE HERE...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')
		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		choice = 3 #anything that is different from 0 so that the game loop goes on

	elif errors > 2: #lost game
		print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	TRY AGAIN LATER,
|     \     \|"""",		WHEN YOU'VE STUDIED
|      \     ______)		THE LESSON BETTER HAHAHA!
\       \  /`
jgs      \(

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		TOO MANY MISTAKES HAHA!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')
		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		errors = 0
		choice = 3 #anything that is different from 0 so that the game loop goes on



	elif correct > 3: #won game
		print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	WE CAN BARELY BELIEVE IT, PILGRIM...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YOU WON...!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')
		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		break

	elif correct == 3: #close win
		print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	THAT WAS A CLOSE CALL...
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		BUT YOU MANAGED...!
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \(

''')
		print("\n"*5)
		input("...	...	...")
		print("\n"*45)
		break

	else:
		continue


#final interaction with the trolls.
#the game only gets to this point, if the user makes less than 3 mistakes
#otherwise the game keeps looping

print(
r'''
        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV	\	 WE UNDERESTIMATED YOU, PILGRIM...
|     \     \|"""",
|      \     ______)		WHAT ARE THE CHANCES, THAT YOU'D HAVE
\       \  /`			A DOTHRAKI VERB DICTIONARY?!
jgs      \(


        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV		YES, WE COULDN'T REALLY EXPECT THAT...
|     \     \|"""",		WELL, WE'RE NOT THAT EVIL. YOU CAN GO YOUR WAY
|      \     ______)		AND TAKE THE DAMN SNAIL WITH YA!
\       \  /`			GO ON, THEN!
jgs      \(

''')

print("\n"*5)
input("...	...	...")
print("\n"*45)


#5. FINAL REVELATIONS
#in this final section, there's one last storytelling bit.
#the snail reveals its real identity and helps our hero
#understanding more of the inscription of the main game

print(
r'''
        THANK YOU!              @             _________
                                 \____       /         \
                                 /    \     /   ____    \
                                 \_    \   /   /    \    \
                                   \    \ (    \__/  )    )
                                    \    \_\ \______/    /
                                     \      \           /___
                                      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
	I WAS EXPECTING YOU!	@             _________
THE ORACLE TOLD ME		 \____       /         \
YOU'D COME TO HELP!		 /    \     /   ____    \
				 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
	SHE ALSO TOLD ME	@             _________
ALL ABOUT YOUR QUEST.		 \____       /         \
				 /    \     /   ____    \
YOU'VE COME A LONG WAY!		 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
PERHAPS I CAN BE OF SOME	@             _________
	HELP TO YOU!		 \____       /         \
I'M WELL-ACQUAINTED WITH	 /    \     /   ____    \
DOTHRAKI VERBS.			 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
THE ORACLE TOLD ME		@             _________
SHE HAD GIVEN YOU MY BOOK!	 \____       /         \
BUT IT'S A VERY BAD COPY	 /    \     /   ____    \
ISN'T IT?			 \_    \   /   /    \    \
				   \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''

DO YOU HAVE THE INSCRIPTION	@             _________
	WITH YOU?		 \____       /         \
	...			 /    \     /   ____    \
I SEE... THERE ARE 3 VERBS	 \_    \   /   /    \    \
	IN THIS INCRIPTION:        \    \ (    \__/  )    )
		[EZATAS]	    \    \_\ \______/    /
		[JOLINATAS]	     \      \           /___
		[AZHATAS]	      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''

THEY'RE ALL IMPERATIVE		@             _________
	FORMS!			 \____       /         \
YOU CAN SEE THAT		 /    \     /   ____    \
	BECAUSE OF THE		 \_    \   /   /    \    \
	MORPHEME [-AS]	           \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)



print(
r'''

[EZATAS]			@             _________
				 \____       /         \
EZAT MEANS			 /    \     /   ____    \
	TO FIND.		 \_    \   /   /    \    \
			           \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''

[JOLINATAS]			@             _________
				 \____       /         \
				 /    \     /   ____    \
JOLINAT MEANS			 \_    \   /   /    \    \
	TO COOK.	           \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)



print(
r'''

[AZHATAS]			@             _________
				 \____       /         \
AZHAT MEANS			 /    \     /   ____    \
	TO GIVE			 \_    \   /   /    \    \
	SOMETHING	           \    \ (    \__/  )    )
	TO SOMEONE.		    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''

				@             _________
				 \____       /         \
				 /    \     /   ____    \
JOLINAT MEANS			 \_    \   /   /    \    \
	TO COOK.	           \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)



print(
r'''

				@             _________
				 \____       /         \
				 /    \     /   ____    \
HOPEFULLY THIS HELPS.		 \_    \   /   /    \    \
		     	           \    \ (    \__/  )    )
				    \    \_\ \______/    /
				     \      \           /___
				      \______\_________/____"-_
''')

print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
		@             _________
		 \____       /         \
		 /    \     /   ____    \
		 \_    \   /   /    \    \
		   \    \ (    \__/  )    )
		    \    \_\ \______/    /
		     \      \           /___
		      \______\_________/____"-_
''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
@             _________
 \____       /         \
 /    \     /   ____    \
 \_    \   /   /    \    \
   \    \ (    \__/  )    )
    \    \_\ \______/    /
     \      \           /___
      \______\_________/____"-_
''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)



print(
r'''
    ___(                        )
   (                          _)
  (_                       __))
    ((                _____)
      (_________)----'
         _/  /
        /  _/
      _/  /
     / __/
   _/ /
  /__/
 //
/'

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	SORRY! I HAD TO MOVE TO BREAK THE SPELL
         (, \_/ \\_/		THAT THE TROLLS HAD PUT ON ME.
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	DON'T BE SO SURPRISED! HOW DO YOU THINK I KNEW THAT STUFF?
         (, \_/ \\_/		WELL... YOU SEE, I'M A LINGUIST MYSELF!
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	AT LEAST I WAS, BEFORE THE TROLLS CAUGHT ME...
         (, \_/ \\_/		THEY WERE ASKING ME QUESTIONS ABOUT PHONETICS...
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	BUT I'M A SEMANTICIST! I TRIED TO TELL THEM,
         (, \_/ \\_/		BUT THEY WOULDN'T LISTEN...
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	I'M RICHARD MONTAGUE, I SAID!
         (, \_/ \\_/		YOUR BEHAVIOUR IS VERY ILLOGICAL, I CRIED...
          |    -' |			YOU SEE, ACCORDING TO THE LAW OF MODUS PONENS...
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	BUT THEY JUST LAUGHED AND SAID:
         (, \_/ \\_/		THAT'S RIGHT HAHAHA...
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)


print(
r'''
         __
           .'  `'.
          /  _    |
          #_/.\==/.\	WELL, ANYWAY... YOU JUST CAN'T ARGUE WITH SOME PEOPLE!
         (, \_/ \\_/		
          |    -' |
          \   '=  /
          /`-.__.'
       .-'`-.___|__
jgs   /    \       `.

''')


print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
                       /\
        _/\           /  \
    _  /   \         /    \/\
   / \/   _ \     /\/\  _  _/\
  /   \_ / \/\_/\/_/  \/ \/   \
 /\/\   \_   /   \/            \
/    \___/\ /     \             \
           \       \             \
           .-"---.  \             \
__..---.. /       \  \             \
         /\___.-'./\''--..____..--''
`-.      \/ O) (O \/ ''--.._
    __    |  (_)  |         _.-'-._	IT SEEMS WE HAVE CLOSED ONE MORE CHAPTER
   / /  __/\\___//\__ ..--''-._
   | (_/\ \/`---'\/ /\         `-._		IN THE LINGUISTIC JOURNEY OF OUR HERO.
_.-\ \/  \  \   /  /  \.-'-._
   /\|   /  -| |-  \   \     `-._	WE NOW KNOW WHAT THE VERBS IN THE INCRIPTION MEAN.
  | ||  /\  -| |-  /\   \        `-.
   \/|_/ |  -|_\-  |/   /		WHAT LIES AHEAD IN THE PILGRIM'S FUTURE?
   \ \   /  /B_B\  \\  /
   / (   \_/  _  \_/ \/				ONLY THE GODS KNOW...
.__\ \   /    |    \_/
   ) /''-| __ | __ |			BUT PERHAPS ANOTHER PIECE OF THE MESSAGE
   |(    \    |    /---...___
   /|    /____|____\         '-._		COULD REVEAL ITSELF IN THE COMING EPISODES...
   ||     |   ||   |
   \\     ///\\//\\\
jro \|   oOO(_)(_)OOo
''')



print("\n"*5)
input("...      ...     ...")
print("\n"*45)

print(
r'''
                       /\
        _/\           /  \
    _  /   \         /    \/\
   / \/   _ \     /\/\  _  _/\
  /   \_ / \/\_/\/_/  \/ \/   \
 /\/\   \_   /   \/            \
/    \___/\ /     \             \
           \       \             \
           .-"---.  \             \
__..---.. /       \  \             \
         /\___.-'./\''--..____..--''
`-.      \/ O) (O \/ ''--.._
    __    |  (_)  |         _.-'-._	
   / /  __/\\___//\__ ..--''-._
   | (_/\ \/`---'\/ /\         `-._		!!THE END!!
_.-\ \/  \  \   /  /  \.-'-._
   /\|   /  -| |-  \   \     `-._	
  | ||  /\  -| |-  /\   \        `-.
   \/|_/ |  -|_\-  |/   /		
   \ \   /  /B_B\  \\  /
   / (   \_/  _  \_/ \/			
.__\ \   /    |    \_/
   ) /''-| __ | __ |			
   |(    \    |    /---...___
   /|    /____|____\         '-._	
   ||     |   ||   |
   \\     ///\\//\\\
jro \|   oOO(_)(_)OOo
''')
