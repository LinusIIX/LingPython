# Assignment 5: The last stand

#TODO Kommentare übersetzen...DAS IST ALLES NOCH TEMPORÄR ALSO NICHT RUMMAULEN DANIEL ^^

#---------------------------------------------
# import necessary modules
import os
import random
import sys

#---------------------------------------------

# Function to clear the console
def clear():

    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("OS not supported")
        sys.exit()

#---------------------------------------------
# "Game assets" -> Heroes, Weapons, Monsters

#TODO Beschreibungen und Werte anpassen

# heroes
# name = (name, health, strength, luck)
Aragorn =           ("Aragorn"  , 10, 1.0, 3) 
Gimli =             ("Gimli"    , 10, 1.0 , 3)
Legolas =           ("Legolas"  , 10, 1.0 , 4)
Frodo =             ("Frodo"    , 10, 1.0 , 5)
Boromir =           ("Boromir"  , 10, 1.0, 0.1)

# tuple with heroes
heroes = (Aragorn, Gimli, Legolas, Frodo, Boromir)  

# weapons
# name = (name, damage, special)
Glamdring =        ("Glamdring" , 3, "special")
Orcrist =          ("Orcrist"   , 3, "Orc"    )
Sting =            ("Sting"     , 3, "special")
Anduril =          ("Anduril"   , 3, "special")
Narsil =           ("Narsil"    , 3, "special")
# tuple with weapons
weapons = (Glamdring, Orcrist, Sting, Anduril, Narsil)

# enemies
# name = (name, health, strength, special)
UrukHai =          ("Uruk-Hai"          , 3, 3 , "special")
Orc =              ("Orc"               , 3, 3 , "special")
Nazgul =           ("Nazgul"            , 3, 3 , "special")
Troll =            ("Troll"             , 3, 3 , "special")
Warg =             ("Warg"              , 3, 3 , "special")
DerBiBaBuzemann =  ("Der BiBaBuzemann"  , 10, 5, "special")
JoeMama =          ("Joe Mama"          , 10, 5, "special")
# tuple with enemies
monster = (UrukHai, Nazgul, Troll, Warg, Orc, DerBiBaBuzemann, JoeMama)

#---------------------------------------------
# Ascii Art

box_width = 73
linuxLogoAscii = '''
       _nnnn_                      
      dGGGGMMb     ,"""""""""""""""""""""""""""""""""""".
     @p~qp~~qMb    | See you soon ^^ (Linux auf die 1!) |
     M|@||@) M|   _;....................................'
     @,----.JM| -'
    JS^\__/  qKL
   dZP        qKRb
  dZP          qKKb
 fZP            SMMb
'''


# Ascii Art for heroes
aragornNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aragorn".center(box_width) + "|\n" + "|" + f"Health: {Aragorn[1]} Strength: {Aragorn[2]} Luck: {Aragorn[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
aragornDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aragorn is the rightful heir to the throne of Gondor.".center(box_width) + "|\n" + "|" + "He is a skilled swordsman and a great leader.".center(box_width) + "|\n" + "|" + f"Health: {Aragorn[1]} Strength: {Aragorn[2]} Luck: {Aragorn[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

gimliNameAscii =            f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Gimli".center(box_width) + "|\n" + "|" + f"Health: {Gimli[1]} Strength: {Gimli[2]} Luck: {Gimli[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
gimliDescriptionAscii =     f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Gimli is a dwarf warrior, son of Glóin.".center(box_width) + "|\n" + "|" + "He is known for his loyalty and bravery.".center(box_width) + "|\n" + "|" + f"Health: {Gimli[1]} Strength: {Gimli[2]} Luck: {Gimli[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

legolasNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Legolas".center(box_width) + "|\n" + "|" + f"Health: {Legolas[1]} Strength: {Legolas[2]} Luck: {Legolas[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
legolasDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Legolas is an elven prince and skilled archer.".center(box_width) + "|\n" + "|" + "He has keen senses and unmatched agility.".center(box_width) + "|\n" + "|" + f"Health: {Legolas[1]} Strength: {Legolas[2]} Luck: {Legolas[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

frodoNameAscii =            f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Frodo".center(box_width) + "|\n" + "|" + f"Health: {Frodo[1]} Strength: {Frodo[2]} Luck: {Frodo[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
frodoDescriptionAscii =     f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Frodo is a hobbit of the Shire.".center(box_width) + "|\n" + "|" + "He is the bearer of the One Ring.".center(box_width) + "|\n" + "|" + f"Health: {Frodo[1]} Strength: {Frodo[2]} Luck: {Frodo[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

boromirNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Boromir".center(box_width) + "|\n" + "|" + f"Health: {Boromir[1]} Strength: {Boromir[2]} Luck: {Boromir[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
boromirDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Boromir is a valiant warrior of Gondor.".center(box_width) + "|\n" + "|" + "He is known for his strength and courage.".center(box_width) + "|\n" + "|" + f"Health: {Boromir[1]} Strength: {Boromir[2]} Luck: {Boromir[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

# Ascii Art for weapons
glamdringNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Glamdring                                 |
|                                                                         |
+-------------------------------------------------------------------------+
"""

glamdringDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

narsilNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                                Narsil                                   |
|                                                                         |
+-------------------------------------------------------------------------+
"""

narsilDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

stingNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                                 Sting                                   |
|                                                                         |
+-------------------------------------------------------------------------+
"""

stingDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

andurilNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                                Anduril                                  |
|                                                                         |
+-------------------------------------------------------------------------+
"""

andurilDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

orcistNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                                Orcrist                                  |
|                                                                         |
+-------------------------------------------------------------------------+
"""

orcistDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

#---------------------------------------------
# Generate random amount of monsters

# random zwischen 1 und 5 -> Anzahl Monster
monsterCount = random.randint(1, 5)
monsterList = []

# Schleife while Anzahl Monster > 0  wähle zufälliges Monster und füge es zu Liste hinzu
while monsterCount > 0:
    monster = random.choice((UrukHai, Nazgul, Troll, Warg, DerBiBaBuzemann, JoeMama)) #evtl. Wahrscheinlichkeit anpassen JoeMama/BiBaBuzemann 1-5% chance oder so 
    monsterList.append(monster)
    monsterCount -= 1

#---------------------------------------------
# Game 
# Explanation of the game:

# TODO: Erklärung des Spiels einfügen

#---------------------------------------------
# Lore/Story

clear()
print("+" + "-" * box_width + "+")
print("| This is an alternative timeline of The Lord of the Rings.               |")
print("| Boromir survived, and the Fellowship never split up. Saruman            |")
print("| sent out a massive army to wipe out the Rohirrim.                       |")
print("| Using dark witchcraft, Saruman destroyed the walls of Helm's            |")
print("| Deep, forcing the Fellowship to defend the fortress.                    |")
print("| The battle was brutal, and the Fellowship could not hold the            |")
print("| fortress. The women and children fled through the mountain path,        |")
print("| while the Fellowship stayed behind to cover their escape.               |")
print("| Saruman's massive army flooded the fortress, and the Fellowship         |")
print("| was separated. Now, they must fight their way through the               |")
print("| fortress to reunite and escape.                                         |")
print("| Choose your hero and fight your way through the fortress to             |")
print("| reunite with the Fellowship and escape.                                 |")
print("+" + "-" * box_width + "+")


#---------------------------------------------
# Loop to choose a hero
# Choosable heroes are "Aragorn", "Gimli", "Legolas", "Frodo" and "Boromir"
# If the user types the name of the hero, the hero is chosen
# If the user types the number of the hero, the user gets more information about the hero
# If the user types "x" the game is exited

chosenHero = None
while chosenHero == None:
    print("")
    print("+" + "-" * box_width + "+")
    print("| Choose your hero by typing the name.                                    |")
    print("| If you want to see more information about a hero,                       |")
    print("| type the corresponding number.                                          |")
    print("+" + "-" * box_width + "+")
    print("| Aragorn (1) | Gimli (2) | Legolas (3) | Frodo (4) | Boromir (5)         |")
    print("+" + "-" * box_width + "+")
    print("| To exit the game, type 'x'                                              |")
    print("+" + "-" * box_width + "+")      
    x = input("")

    match x:
        case "1":
            clear()
            print(aragornDescriptionAscii)
            
        case "2":
            clear()
            print(gimliDescriptionAscii)

        case "3":
            clear()
            print(legolasDescriptionAscii)
            
        case "4":
            clear()
            print(frodoDescriptionAscii)
            
        case "5":
            clear()
            print(boromirDescriptionAscii)
        case "x":
            clear()
            print(linuxLogoAscii)
            sys.exit()

        case "Aragorn":
            chosenHero = Aragorn
            break
        case "Gimli":
            chosenHero = Gimli
            break
        case "Legolas":
            chosenHero = Legolas
            break
        case "Frodo":
            chosenHero = Frodo
            break
        case "Boromir":
            chosenHero = Boromir
            break  

        case _:
            clear()
            print("+" + "-" * box_width + "+")
            print("|" + " "* box_width + "|")
            print("|" + "Wrong Input!".center(box_width) + "|")
            print("|" + " "* box_width + "|")
            print("+" + "-" * box_width + "+")

#---------------------------------------------    
# Loop to choose a weapon
y = "0"
chosenWeapon = None
while chosenWeapon == None: 
    
    clear()
    x = y
    match chosenHero[0]:
        case "Aragorn":
            print(aragornNameAscii)
        case "Gimli":
            print(gimliNameAscii)
        case "Legolas":
            print(legolasNameAscii)
        case "Frodo":
            print(frodoNameAscii)
        case "Boromir":
            print(boromirNameAscii)
    
    match x:
        case "0":
            print("+" + "-" * box_width + "+")
            print("|" + " "* box_width + "|")
            print("|" + "Choose your weapon!".center(box_width) + "|")
            print("|" + " "* box_width + "|")
            print("+" + "-" * box_width + "+")
        case "1":
            print(glamdringDescriptionAscii)
        case "2":
            print(orcistDescriptionAscii)
        case "3":
            print(stingDescriptionAscii)
        case "4":
            print(andurilDescriptionAscii)
        case "5":
            print(narsilDescriptionAscii)

    print("")
    print("+" + "-" * box_width + "+")
    print("| Choose your weapon by typing the name.                                  |")
    print("| If you want to see more information about a weapon,                     |")
    print("| type the corresponding number.                                          |")
    print("+" + "-" * box_width + "+")
    print("| Glamdring (1) | Orcrist (2) | Sting (3) | Anduril (4) | Narsil (5)      |")
    print("+" + "-" * box_width + "+")
    print("| To exit the game, type 'x'                                              |")
    print("+" + "-" * box_width + "+")
    y = input("")

    match y:
        case "x":
            clear()
            print(linuxLogoAscii)
            sys.exit()
        case "Glamdring":
            chosenweapon = Glamdring
            break
        case "Orcrist":
            chosenweapon = Orcrist
            break
        case "Sting":
            chosenweapon = Sting
            break
        case "Anduril":
            chosenweapon = Anduril
            break
        case "Narsil":
            chosenweapon = Narsil
            break
        case _:
            print("+" + "-" * box_width +                   "+")
            print("|" + " "* box_width +                    "|")
            print("|" + "Wrong Input!".center(box_width) +  "|")
            print("|" + " "* box_width +                    "|")
            print("+" + "-" * box_width +                   "+")

#---------------------------------------------
# Battle Loop

# Editable stats of the hero
heroStats = []
# [health, damage, luck]
heroStats.append(chosenHero[1]).append(chosenHero[2]).append(chosenHero[3])
heroStats[2] = heroStats[2] * chosenWeapon[1]

# Editable stats of the monster
monsterHealth = []
for monster in monsterList:
    monsterHealth.append(monster[1])

while len(monsterList) > 0: 

    clear()
    print("+" + "-" * box_width + "+")
    print("|                                                                         |")
    print(f"|" + "The battle begins!".center(box_width) + "|")
    print("|                                                                         |")
    print("+" + "-" * box_width + "+")
    print("")

    print("+" + "-" * box_width + "+")
    print("|" + " ".center(box_width) + "|")
    print("|" + f"You chose {chosenHero[0]} with {chosenweapon[0]}!".center(box_width) + "|")
    print("|" + f"You are facing {len(monsterList)} monster(s)!".center(box_width) + "|")
    print("|" + " ".center(box_width) + "|")
    print("+" + "-" * box_width + "+")

    monster = monsterList[0]
    print("+" + "-" * box_width + "+")
    print("|" + " ".center(box_width) + "|")
    print("|" + f"You are facing {monster[0]}!".center(box_width) + "|")
    print("|" + " ".center(box_width) + "|")
    print("+" + "-" * box_width + "+")
    print("|" +"Attack (1) | Try to Heal (2)".center(box_width) + "|")
    print("+" + "-" * box_width + "+")
    
    x = input("")

    if x == "1":
        print("+" + "-" * box_width + "+")
        print("|" + "You choose to attack!".center(box_width) + "|")
        print("|" + ("You hit the monster and dealt " + str(heroStats[2]) + " damage").center(box_width) + "|")
        print("+" + "-" * box_width + "+")

    monsterList.pop(0)