# Assignment 5

# Luca Pomm, Linus Prange, Daniel Shaw, Nils Schiele

#---------------------------------------------
# Exercise 5.1 - Line: 151
# Exercise 5.2 - Line: 539
#---------------------------------------------
# import necessary modules

# os is mainly used to clear the console
import os 
# random is used to generate random numbers
import random
# sys is used to exit the game properly
import sys

#---------------------------------------------

# Function to clear the console
# os.name is used to determine the operating system
# "nt" is used for Windows and posix is used for Unix/Linux
def clear():

    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("OS not supported")
        sys.exit()

#---------------------------------------------
#Game "Assets" and Ascii Art

# Constants:

# Width of the boxes for the heroes, weapons and enemies
box_width = 73

# Heroes: Line 47
# Weapons: Line 57
# Enemies: Line 68

# Heroes:
# name = (name, health, strength, luck)
Aragorn =           ("Aragorn"  , 9, 1.2, 6) 
Gimli =             ("Gimli"    , 15, 0.9 , 4)
Legolas =           ("Legolas"  , 8, 1.5 , 5)
Frodo =             ("Frodo"    , 11, 0.5 , 8)
Boromir =           ("Boromir"  , 20, 1.6, 2)
# tuple containing heroes
heroes = (Aragorn, Gimli, Legolas, Frodo, Boromir)  

# Weapons:
# name = (name, damage, parry strength, special)
# "special" could be a future feature(probably not)
Belthronding =     ("Belthronding"  , 5, 2, "special")
Orcrist =          ("Orcrist"       , 4, 3, "special")
Sting =            ("Sting"         , 2, 6, "special")
Aeglos =           ("Aeglos"        , 8, 2, "special")
Narsil =           ("Narsil"        , 3, 4, "special")
# tuple containing weapons
weapons = (Belthronding, Orcrist, Sting, Aeglos, Narsil)

# Enemies:
# name = (name, health, strength, special)
# "special" could be a future feature
UrukHai =          ("Uruk-Hai"          , 7, 3 , "special")
Orc =              ("Orc"               , 6, 3 , "special")
Nazgul =           ("Nazgul"            , 12, 6 , "special")
Troll =            ("Troll"             , 7, 2 , "special")
Warg =             ("Warg"              , 8, 4 , "special")
DerBiBaBuzemann =  ("der BiBaBuzemann"  , 20, 5, "special")

# tuple containing enemies
monster = (UrukHai, Nazgul, Troll, Warg, Orc, DerBiBaBuzemann)

#---------------------------------------------

# Fun little ascii art for the Linux Logo (very important)

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

#---------------------------------------------
# Ascii Art for heroes
# "name"NameAscii contains a box with the name of the hero, as well as the health, strength and luck
# "name"DescriptionAscii contains a box with a brief description of the hero

aragornNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aragorn".center(box_width) + "|\n" + "|" + f"Health: {Aragorn[1]} Strength: {Aragorn[2]} Luck: {Aragorn[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
aragornDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aragorn is the rightful heir to the throne of Gondor.".center(box_width) + "|\n" + "|" + "He is a skilled swordsman and a great leader.".center(box_width) + "|\n" + "|" + f"Health: {Aragorn[1]} Strength: {Aragorn[2]} Luck: {Aragorn[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

gimliNameAscii =            f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Gimli".center(box_width) + "|\n" + "|" + f"Health: {Gimli[1]} Strength: {Gimli[2]} Luck: {Gimli[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
gimliDescriptionAscii =     f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Gimli is a dwarf warrior, son of Glóin.".center(box_width) + "|\n" + "|" + "He is known for his loyalty and bravery.".center(box_width) + "|\n" + "|" + f"Health: {Gimli[1]} Strength: {Gimli[2]} Luck: {Gimli[3]}".center(box_width)                         + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

legolasNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Legolas".center(box_width) + "|\n" + "|" + f"Health: {Legolas[1]} Strength: {Legolas[2]} Luck: {Legolas[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
legolasDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Legolas is an elven prince and skilled archer.".center(box_width) + "|\n" + "|" + "He has keen senses and unmatched agility.".center(box_width) + "|\n" + "|" + f"Health: {Legolas[1]} Strength: {Legolas[2]} Luck: {Legolas[3]}".center(box_width)           + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

frodoNameAscii =            f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Frodo".center(box_width) + "|\n" + "|" + f"Health: {Frodo[1]} Strength: {Frodo[2]} Luck: {Frodo[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
frodoDescriptionAscii =     f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Frodo is a hobbit of the Shire.".center(box_width) + "|\n" + "|" + "He is the bearer of the One Ring.".center(box_width) + "|\n" + "|" + f"Health: {Frodo[1]} Strength: {Frodo[2]} Luck: {Frodo[3]}".center(box_width)                                        + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

boromirNameAscii =          f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Boromir".center(box_width) + "|\n" + "|" + f"Health: {Boromir[1]} Strength: {Boromir[2]} Luck: {Boromir[3]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
boromirDescriptionAscii =   f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Boromir is a valiant warrior of Gondor.".center(box_width) + "|\n" + "|" + "He is known for his strength and courage.".center(box_width) + "|\n" + "|" + f"Health: {Boromir[1]} Strength: {Boromir[2]} Luck: {Boromir[3]}".center(box_width)                  + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"


# Ascii Art for weaponName and weaponDescription
# "name"NameAscii contains a box with the name of the weapon, as well as the damage
# "name"DescriptionAscii contains a box with a brief description of the weapon

belthrondingNameAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Belthronding".center(box_width) + "|\n" + "|" + f"Damage: {Belthronding[1]} Parry Strength: {Belthronding[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
belthrondingDescriptionAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Belthronding is a powerful bow made of black Elven wood.".center(box_width) + "|\n" + "|" + "It was wielded by Beleg Cúthalion, the great archer.".center(box_width) + "|\n" + "|" + f"Damage: {Belthronding[1]} Parry Strength: {Belthronding[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

orcistNameAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Orcrist".center(box_width) + "|\n" + "|" + f"Damage: {Orcrist[1]} Parry Strength: {Orcrist[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
orcistDescriptionAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Orcrist is a sword found by Thorin Oakenshield in the trolls' cave.".center(box_width) + "|\n" + "|" + "It is an Elven blade known as the \"Biter\" by the Orcs.".center(box_width) + "|\n" + "|" + f"Damage: {Orcrist[1]} Parry Strength: {Orcrist[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

stingNameAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Sting".center(box_width) + "|\n" + "|" + f"Damage: {Sting[1]} Parry Strength: {Sting[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
stingDescriptionAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Sting is a dagger found by Bilbo Baggins".center(box_width) + "|\n" + "|" + "in the cave of the spiders of Rhûn.".center(box_width) + "|\n" + "|" + "It was wielded by Frodo Baggins in the".center(box_width) + "|\n" + "|" + "battles against the Orcs and the Nazgûl.".center(box_width) + "|\n" + "|" + f"Damage: {Sting[1]} Parry Strength: {Sting[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

aeglosNameAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aeglos".center(box_width) + "|\n" + "|" + f"Damage: {Aeglos[1]} Parry Strength: {Aeglos[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
aeglosDescriptionAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Aeglos is a spear wielded by Gil-galad,".center(box_width) + "|\n" + "|" + "the last High King of the Noldor.".center(box_width) + "|\n" + "|" + "The spear was used by Gil-galad in the".center(box_width) + "|\n" + "|" + "Battle of the Last Alliance against Sauron.".center(box_width) + "|\n" + "|" + f"Damage: {Aeglos[1]} Parry Strength: {Aeglos[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

narsilNameAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Narsil".center(box_width) + "|\n" + "|" + f"Damage: {Narsil[1]} Parry Strength: {Narsil[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"
narsilDescriptionAscii = f"+" + "-" * box_width + "+\n" + "|" + " "*box_width + "|\n" + "|" + "Narsil is a sword wielded by Elendil,".center(box_width) + "|\n" + "|" + "the High King of Arnor and Gondor.".center(box_width) + "|\n" + "|" + "The sword was used by Elendil in the".center(box_width) + "|\n" + "|" + "Battle of the Last Alliance against Sauron.".center(box_width) + "|\n" + "|" + f"Damage: {Narsil[1]} Parry Strength: {Narsil[2]}".center(box_width) + "|\n" + "|" + " "*box_width + "|\n" + "+" + "-" * box_width + "+\n"

#---------------------------------------------

# Main Menu
# The user can choose between two subexercises or exit the program

print("+" + "-" * 73 + "+")
print("|" + "Exercise 5".center(box_width) + "|")
print("+" + "-" * 73 + "+")
print("|" + "Press (1) vor subexercise 1".center(box_width) + "|")
print("|" + "Press (2) vor subexercise 2".center(box_width) + "|")
print("|" + "Press (x) to exit".center(box_width) + "|")
print("+" + "-" * 73 + "+")

x = input("")
if x == "1":

    # Exercise 5.1

    #---------------------------------------------
    # Generate random amount of monsters

    monsterPool = [UrukHai, Nazgul, Troll, Warg, Orc, DerBiBaBuzemann]
    # random zwischen 1 und 5 -> Anzahl Monster
    monsterCount = random.randint(1, 5)
    # list to store the monsters the user has to fight against
    monsterList = []
    
    # use random.choices to choose the monsters the user has to fight against
    monsterList = random.choices(monsterPool, weights = [0.2,0.04,0.2,0.2,0.35,0.01], k=monsterCount)

    #---------------------------------------------
    # Game 
    # Explanation of the game:

    # 1. The user gets a brief explanation of the lore of the game
    # 2. The user chooses a hero from the list of heroes
    # 3. The user chooses a weapon from the list of weapons
    # 4. The user fights against the monsters until all monsters are defeated or the hero dies
    
    #---------------------------------------------
    
    # The user is greeted with a box containing the story of the game
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
                waitForExit = input("Press Enter to continue...")
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
    # Choosable weapons are "Belthronding", "Orcrist", "Sting", "Aeglos" and "Narsil"
    # If the user types the name of the weapon, the weapon is chosen
    # If the user types the number of the weapon, the user gets more information about the weapon
    # If the user types "x" the game is exited

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
                print(belthrondingDescriptionAscii)
            case "2":
                print(orcistDescriptionAscii)
            case "3":
                print(stingDescriptionAscii)
            case "4":
                print(aeglosDescriptionAscii)
            case "5":
                print(narsilDescriptionAscii)
            case _:
                print("+" + "-" * box_width +                   "+")
                print("|" + " "* box_width +                    "|")
                print("|" + "Wrong Input!".center(box_width) +  "|")
                print("|" + " "* box_width +                    "|")
                print("+" + "-" * box_width +                   "+")

        print("")
        print("+" + "-" * box_width + "+")
        print("| Choose your weapon by typing the name.                                  |")
        print("| If you want to see more information about a weapon,                     |")
        print("| type the corresponding number.                                          |")
        print("+" + "-" * box_width + "+")
        print("| Belthronding (1) | Orcrist (2) | Sting (3) | Aeglos (4) | Narsil (5)    |")
        print("+" + "-" * box_width + "+")
        print("| To exit the game, type 'x'                                              |")
        print("+" + "-" * box_width + "+")
        y = input("")

        match y:
            case "x":
                clear()
                print(linuxLogoAscii)
                waitForExit = input("Press Enter to continue...")
                sys.exit()
            case "Belthronding":
                chosenWeapon = Belthronding 
                break
            case "Orcrist":
                chosenWeapon = Orcrist
                break
            case "Sting":
                chosenWeapon = Sting
                break
            case "Aeglos":
                chosenWeapon = Aeglos
                break
            case "Narsil":
                chosenWeapon = Narsil
                break
            case _:
                print("+" + "-" * box_width +                   "+")
                print("|" + " "* box_width +                    "|")
                print("|" + "Wrong Input!".center(box_width) +  "|")
                print("|" + " "* box_width +                    "|")
                print("+" + "-" * box_width +                   "+")

    #---------------------------------------------
    # Battle Loop
    # The battle loop is used to simulate the battle between the hero and the monsters
    # The hero has to fight against the monsters until all monsters are defeated or the hero dies
    # The user can choose between attacking the monster or trying to heal himself (if the user types x, the game is quit)

    # If the user chooses to attack the monster, the hero has a chance to hit the monster, if the random number is smaller or equal to the luck of the hero
    # the hero hits the monster and deals damage to the monster. The hero also has a chance to get hit by the monster, if the random number is smaller or equal to the parry strength of the weapon, the monster fails to hit the hero

    # If the user chooses to try to heal himself, the hero has a chance to heal himself, if the random number is smaller or equal to the luck of the hero, the hero heals himself by 3 health

    # The game ends if the health of the hero is smaller or equal to 0 or if all monsters are defeated

    #---------------------------------------------
    # Create editable stats of the hero from the tuple chosenHero
    # [health, strength, luck]
    myHeroStats = []
    myHeroStats.append(chosenHero[1])
    myHeroStats.append(chosenHero[2])
    myHeroStats.append(chosenHero[3])
    #round so that there arent weird decimals
    myHeroStats[1] = round(myHeroStats[1] * int(chosenWeapon[1]))

    # Create editable health stats of the monsters from the tuple monsterList
    monsterHealth = []
    for monster in monsterList:
        monsterHealth.append(monster[1])


    while len(monsterList) > 0 and myHeroStats[0] > 0: 

        # Clear the console
        clear()

        # Display a box with the text "The battle begins!" 
        print( "+" + "-" * box_width + "+")
        print( "|"+ " "* box_width + "|")
        print(f"|" + "The battle begins!".center(box_width) + "|")
        print( "|"+ " "* box_width + "|")
        print( "+" + "-" * box_width + "+")

        # Display a box with the stats of the hero and the chosen weapon
        print("+" +  "-" * box_width + "+")
        print("|" +  " ".center(box_width) + "|")
        print("|" + f"You chose {chosenHero[0]} with {chosenWeapon[0]}!".center(box_width) + "|")
        print("|" + f"Hero Health: {myHeroStats[0]} | Damage: {myHeroStats[1]} | Luck: {myHeroStats[2]}".center(box_width) + "|")
        print("|" + f"Parry Strength: {chosenWeapon[2]}".center(box_width) + "|")
        print("|" +  " ".center(box_width) + "|")
        print("+" +  "-" * box_width + "+")

        # Display a box with the stats of the current monster as well as the amount of monsters left and the options available to the user
        currentMonster = monsterList[-1]
        print("+" +  "-" * box_width + "+")
        print("|" +  " ".center(box_width) + "|")
        print("|" + f"{len(monsterList)} monster(s) left!".center(box_width) + "|")
        print("|" +  " ".center(box_width) + "|")
        print("|" + f"You are facing {currentMonster[0]}!".center(box_width) + "|")
        print("|" + f"Remaining health: {monsterHealth[-1]}".center(box_width) + "|")
        print("|" +  " ".center(box_width) + "|")
        print("+" +  "-" * box_width + "+")
        print("|" +  "Attack (1) | Try to Heal (2) | Exit (x)".center(box_width) + "|")
        print("+" +  "-" * box_width + "+")
        
        # Wait for the user to input a command
        x = input("")

        # Check the input of the user
        match x:

            # if the user chooses to exit the game
            case "x":

                clear()
                print(linuxLogoAscii)
                waitForExit = input("Press Enter to continue...")
                sys.exit()

            # if the user chooses to attack the monster
            case "1":

                print("+" + "-" * box_width + "+")
                print("|" + "You choose to attack!".center(box_width) + "|")
                
                # Calculate the chance to hit the monster
                randomCheckHit = random.randint(1, 10)

                # Calculate the chance to get hit by the monster
                randomMonsterHit = random.randint(1, 10)

                # if the random number is smaller or equal to the luck of the hero, the hero hits the monster
                if randomCheckHit <= chosenHero[3]:

                    print("|" + ("You hit the monster and dealt " + str(myHeroStats[1]) + " damage").center(box_width) + "|")
                    # subtract the damage of the hero from the health of the current monster
                    monsterHealth[-1] -= myHeroStats[1]

                else:

                    # if the random number is greater than the luck of the hero, the hero misses the monster 
                    print("|" + "You missed the monster".center(box_width) + "|")
                            
                # if the random number is smaller or equal to the parry strength of the weapon, the monster fails to hit the hero
                if randomMonsterHit <= chosenWeapon[2]:
                    print("|" + "The monster failed to hit you".center(box_width) + "|")
                # if the random number is greater than the parry strength of the weapon, the monster hits the hero
                else:        
                    print("|" + f"The monster hit you for 2 damage".center(box_width) + "|")
                    myHeroStats[0] -= 2

                print("+" + "-" * box_width + "+")
                
                # if the health of the current monster is smaller or equal to 0, the monster is defeated
                if monsterHealth[-1] <= 0:
                    print("+" + "-" * box_width + "+")
                    print("|" + "The monster is defeated!".center(box_width) + "|")
                    print("|" + " ".center(box_width) + "|")
                    print("+" + "-" * box_width + "+")
                    monsterHealth.pop()
                    monsterList.pop()   

            # if the user chooses to try to heal himself
            case "2":
                    
                print("+" + "-" * box_width + "+")
                print("|" + "You choose to try to heal!".center(box_width) + "|")

                # Calculate the chance to heal the hero
                randomCheckHeal = random.randint(1, 10)

                # if the random number is smaller or equal to the luck of the hero, the hero heals himself by 3 health and the monster fails to hit the hero
                if randomCheckHeal <= chosenHero[3]:
                    print("|" + "You healed yourself for 3 health!".center(box_width) + "|")
                    print("|" + "The monster failed to hit you".center(box_width) + "|")
                    print("+" + "-" * box_width + "+")
                    myHeroStats[0] += 3
                # if the random number is greater than the luck of the hero, the hero fails to heal himself and the monster hits the hero
                else:
                    print("|" + "You tried to heal yourself but failed!".center(box_width) + "|")
                    print("|" + f"The monster hit you for {currentMonster[2]} damage".center(box_width) + "|")
                    print("+" + "-" * box_width + "+")
                    myHeroStats[0] -= currentMonster[2]

            # if the user types something else display "Wrong Input!"
            case _:
                print("+" + "-" * box_width + "+")
                print("|" + "Wrong Input!".center(box_width) + "|")
                print("+" + "-" * box_width + "+")
                continue

        waitForExit = input("Press Enter to continue...")

    #---------------------------------------------
    # End of the game

    # If the health of the hero is smaller or equal to 0, the hero dies and the corresponding message is displayed
    if myHeroStats[0] <= 0:
        clear()
        print("+" + "-" * box_width + "+")
        print("|" + " ".center(box_width) + "|")
        print("|" + "You died!".center(box_width) + "|")
        print("|" + "The fellowship was able to escape, but you were left behind.".center(box_width) + "|")
        print("|" + " ".center(box_width) + "|")
        print("+" + "-" * box_width + "+")
        # wait for the user to press any key to exit the program
        waitForExit = input("Press any key to exit...")
        sys.exit()
    else:
        # If the health of the hero is greater than 0, the hero wins the game and the corresponding message is displayed
        clear()
        print("+" + "-" * box_width + "+")
        print("|" + " ".center(box_width) + "|")
        print("|" + "Congratulations!".center(box_width) + "|")
        print("|" + "You defeated all the monsters and reunited with the fellowship.".center(box_width) + "|")
        print("|" + "The women and children were able to escape through the mountain path.".center(box_width) + "|")
        print("|" + "The fortress was lost, but the war is not over.".center(box_width) + "|")
        print("|" + "As long as there is hope, there is a chance for victory.".center(box_width) + "|")
        print("|" + " ".center(box_width) + "|")
        print("+" + "-" * box_width + "+")
        # wait for the user to press any key to exit the program
        waitForExit = input("Press any key to exit...")
        sys.exit()

elif x == "2":
    
    # Exercise 5.2

    # Random Nouns and Adjectives
    nouns = ("Kopf", "Baum", "Pflanze", "Katze", "Hund", "Sonne", "Tonne", "Berg", "Topf", "Wasser", "Hahn", "Huhn", "Kraut", "Schlauch", "Schuh", "Kuh", "Maus", "Haus", "Maus", "Strauch", "Kraut")
    adjective = ("rot", "blau", "feucht", "hell", "hart", "leicht", "voll", "hoch", "interaktiv, " "schnell", "langsam", "warm", "kalt", "scharf", "weich")


    print("To quit the program type 'quit'")
    while True:

        inStr = input("Type a noun or an adjective (nouns are starting with a capital letter):")
        # Check if the user wants to quit the program
        if inStr == "quit":
            break
        
        if inStr != "":
            additionalWord = ""
            # Check if the input is a noun or an adjective
            if inStr[0].isupper():
                # if the input is an adjective choose a random noun from the list
                idx = random.randint(0, len(adjective)-1)
                additionalWord = adjective[idx]
                print(additionalWord + inStr.lower())
            else:
                # if the input is a noun choose a random adjective from the list
                idx = random.randint(0, len(nouns)-1)
                additionalWord = nouns[idx]
                print(inStr + additionalWord.lower())

elif x == "x":
    clear()
    print(linuxLogoAscii)
    # wait for the user to press any key to exit the program
    waitForExit = input("Press any key to exit...")
    sys.exit()
else:
    clear()
    print("+" + "-" * box_width + "+")
    print("|" + "Wrong Input!".center(box_width) + "|")
    print("+" + "-" * box_width + "+")
    # wait for the user to press any key to exit the program
    waitForExit = input("Press any key to exit...")
    sys.exit()