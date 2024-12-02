# Assignment 5: Battle of the 5 "or less" armies

#TODO Kommentare übersetzen...DAS IST ALLES NOCH TEMPORÄR ALSO NICHT RUMMAULEN DANIEL ^^

import random

#---------------------------------------------
# "Game assets" -> Heroes, Weapons, Monsters

#TODO Beschreibungen und Werte anpassen
# Helden
# health, strength, luck durch Werte austauschen
Aragorn = ("Aragorn", "Beschreibung", "health", "strength", 3) 
Gimli = ("Gimli", "Beschreibung", "health", "strength", 3)
Legolas = ("Legolas", "Beschreibung", "health", "strength", 4)
Frodo = ("Frodo", "Beschreibung", "health", "strength", 5)
Boromir = ("Boromir", "Beschreibung", "health", "strength", 0)
# tuple mit Helden
heroes = (Aragorn, Gimli, Legolas, Frodo, Boromir)  

# Waffen
# damage, special durch Werte austauschen
Glamdring = ("Glamdring", "Beschreibung", "damage", "special")
Orcrist = ("Orcrist", "Beschreibung", "damage", "special")
Sting = ("Sting", "Beschreibung", "damage", "special")
Anduril = ("Anduril", "Beschreibung", "damage", "special")
Narsil = ("Narsil", "Beschreibung", "damage", "special")
# tuple mit Waffen
weappons = (Glamdring, Orcrist, Sting, Anduril, Narsil)

# Monster
UrukHai = ("Uruk-Hai", "Beschreibung", "health", "strength", "special")
Nazgul = ("Nazgul", "Beschreibung", "health", "strength", "special")
Troll = ("Troll", "Beschreibung", "health", "strength", "special")
Warg = ("Warg", "Beschreibung", "health", "strength", "special")
DerBiBaBuzemann = ("Der BiBaBuzemann", "Beschreibung", "health", "strength", "special")
JoeMama = ("Joe Mama", "Beschreibung", "health", "strength", "special")
# Tuple mit Monstern
monster = (UrukHai, Nazgul, Troll, Warg, DerBiBaBuzemann, JoeMama)

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
# TODO: Lore/Story einfügen

print("Welcome to the Battle of the 5 (or less) Armies!")
print("You can choose between the following heroes:")


#---------------------------------------------
# Loop to choose a hero
# Choosable heroes are "Aragorn", "Gimli", "Legolas", "Frodo" and "Boromir"
# If the user types the name of the hero, the hero is chosen
# If the user types the number of the hero, the user gets more information about the hero
# If the user types "x" the game is exited

chosenHero = None
while chosenHero == None:
        
    i=0
    for hero in heroes:
        i+=1
        print(hero[0]+ " (" + str(i) + ")")

    print("To choose a hero type the name of the hero")
    x = input("See more information of a hero type the corresponding number (1-5) or exit with (x): ")

    match x:
        case "1":
            print("\nText Aragorn\n")
        case "2":
            print("\nText Gimli\n")
        case "3":
            print("\nText Legolas\n")
        case "4":
            print("\nText Frodo\n")
        case "5":
            print("\nText Boromir\n")
        case "x":
            print("See you soon ^^ ")
            break

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
            print("wrong input")

#---------------------------------------------    

              



#---------------------------------------------
# Battle Loop

# TODO Battle Schleife solange noch Monster in der Liste wähle erstes und simuliere Kampf -> wenn Monster tot entferne es aus Liste, sonst losingscreen
while len(monsterList) > 0: 
    monster = monsterList[0]
    # Kampf simulieren
    # Wenn Monster tot -> entferne aus Liste
    # Wenn Monster nicht tot -> losingscreen
    monsterList.pop(0)