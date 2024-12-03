# Assignment 5: The last stand

#TODO Kommentare übersetzen...DAS IST ALLES NOCH TEMPORÄR ALSO NICHT RUMMAULEN DANIEL ^^

#---------------------------------------------
# import necessary modules
import os
import random

#---------------------------------------------

# Function to clear the console
def clear():

    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("OS not supported")
        exit()

#---------------------------------------------
# "Game assets" -> Heroes, Weapons, Monsters

#TODO Beschreibungen und Werte anpassen

# heroes
# name = (name, description, health, strength, luck)
Aragorn = ("Aragorn", "description", 10, 1.0, 3) 
Gimli = ("Gimli", "description", 10, 1.0 , 3)
Legolas = ("Legolas", "description", 10, 1.0 , 4)
Frodo = ("Frodo", "description", 10, 1.0 , 5)
Boromir = ("Boromir", "description", 10, 1.0, 0.1)

# tuple with heroes
heroes = (Aragorn, Gimli, Legolas, Frodo, Boromir)  

# weapons
# name = (name, description, damage, special)
Glamdring = ("Glamdring", "description", 3, "special")
Orcrist = ("Orcrist", "description", 3, "Orc")
Sting = ("Sting", "description", 3, "special")
Anduril = ("Anduril", "description", 3, "special")
Narsil = ("Narsil", "description", 3, "special")
# tuple with weapons
weapons = (Glamdring, Orcrist, Sting, Anduril, Narsil)

# enemies
UrukHai = ("Uruk-Hai", "description", "health", "strength", "special")
Orc = ("Orc", "description", "health", "strength", "special")
Nazgul = ("Nazgul", "description", "health", "strength", "special")
Troll = ("Troll", "description", "health", "strength", "special")
Warg = ("Warg", "description", "health", "strength", "special")
DerBiBaBuzemann = ("Der BiBaBuzemann", "description", "health", "strength", "special")
JoeMama = ("Joe Mama", "description", "health", "strength", "special")
# tuple with enemies
monster = (UrukHai, Nazgul, Troll, Warg, Orc, DerBiBaBuzemann, JoeMama)

#---------------------------------------------
# Ascii Art

box_width = 73
seeYouSoonAscii = """
                                                                                                                                           .--,            .--,       
                                                                                                                                          :   /\          :   /\      
  .--.--.                                                                                                                                /   ,  \        /   ,  \     
 /  /    '.                                                                                                                             /   /    \      /   /    \    
|  :  /`. /                                          ,---.           ,--,                       ,---.     ,---.        ,---,           ;   /  ,   \    ;   /  ,   \   
;  |  |--`                                          '   ,'\        ,'_ /|           .--.--.    '   ,'\   '   ,'\   ,-+-. /  |         /   /  / \   \  /   /  / \   \  
|  :  ;_       ,---.     ,---.                .--, /   /   |  .--. |  | :          /  /    '  /   /   | /   /   | ,--.'|'   |        /   ;  /\  \   \/   ;  /\  \   \ 
 \  \    `.   /     \   /     \             /_ ./|.   ; ,. :,'_ /| :  . |         |  :  /`./ .   ; ,. :.   ; ,. :|   |  ,"' |        \"""\ /  \  \ ; \"""\ /  \  \ ;  
  `----.   \ /    /  | /    /  |         , ' , ' :'   | |: :|  ' | |  . .         |  :  ;_   '   | |: :'   | |: :|   | /  | |         `---`    `--`   `---`    `--`   
  __ \  \  |.    ' / |.    ' / |        /___/ \: |'   | .; :|  | ' |  | |          \  \    `.'   | .; :'   | .; :|   | |  | |                                         
 /  /`--'  /'   ;   /|'   ;   /|         .  \  ' ||   :    |:  | : ;  ; |           `----.   \   :    ||   :    ||   | |  |/                                          
'--'.     / '   |  / |'   |  / |          \  ;   : \   \  / '  :  `--'   \         /  /`--'  /\   \  /  \   \  / |   | |--'                                           
  `--'---'  |   :    ||   :    |           \  \  ;  `----'  :  ,      .-./        '--'.     /  `----'    `----'  |   |/                                               
             \   \  /  \   \  /             :  \  \          `--`----'              `--'---'                     '---'                                                
              `----'    `----'               \  ' ;                                                                                                                   
                                              `--`                                                                                                                    
"""

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
aragornNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Aragorn                                   |
|                                                                         |
+-------------------------------------------------------------------------+
"""

aragornDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

gimliNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Gimli                                     |
|                                                                         |
+-------------------------------------------------------------------------+
"""

gimliDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

legolasNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Legolas                                   |
|                                                                         |
+-------------------------------------------------------------------------+
"""

legolasDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

frodoNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Frodo                                     |
|                                                                         |
+-------------------------------------------------------------------------+
"""

frodoDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

boromirNameAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
|                               Boromir                                   |
|                                                                         |
+-------------------------------------------------------------------------+
"""

boromirDescriptionAscii = """
+-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
"""

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
            exit()

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
            exit()

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
            
            print("+" + "-" * box_width + "+")
            print("|" + " "* box_width + "|")
            print("|" + "Wrong Input!".center(box_width) + "|")
            print("|" + " "* box_width + "|")
            print("+" + "-" * box_width + "+")
    
    

#---------------------------------------------
# Battle Loop

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
print("|" + f"You are facing {len(monsterList)} monsters!".center(box_width) + "|")
print("|" + " ".center(box_width) + "|")
print("+" + "-" * box_width + "+")




# TODO Battle Schleife solange noch Monster in der Liste wähle erstes und simuliere Kampf -> wenn Monster tot entferne es aus Liste, sonst losingscreen
while len(monsterList) > 0: 
    monster = monsterList[0]
    # Kampf simulieren
    # Wenn Monster tot -> entferne aus Liste
    # Wenn Monster nicht tot -> losingscreen
    monsterList.pop(0)