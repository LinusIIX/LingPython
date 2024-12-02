# Assignment 5: Battle of the 5 "or less" armies

import random

#---------------------------------------------
# assets

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

# Explanation text

# Schleife zur Heldenwahl -> User wird liste mit helden angezeigt mit entsprechenden Buchstaben kann er sich mehr Informationen anzeigen lassen -> In Informationen Screen kann er zurück zu auswahl oder game starten
x = "werDasLiestIstDoof"
while x != "x":
    
    print("Welcome to the Battle of the 5 (or less) Armies!")
    print("You can choose between the following heroes:")
    
    i=0
    for hero in heroes:
        i+=1
        print(hero[0]+ " (" + str(i) + ")")
    x = input("Choose your hero with (1-5) or exit(x): ")


    match x:
    case "1":
        print("Text Aragorn")
    case "2":
        print("Text Gimli")
    case "3":
        print("Text Legolas")
    case "4":
        print("Text Frodo")
    case "5":
        print("Text Boromir")
    case _:
        print("wrong input")

              

# Text -> Du begegnest x Monstern 
print("Du begegnest", len(monsterList), "Monstern") #anpassen


# Battle Schleife solange noch Monster in der Liste wähle erstes und simuliere Kampf -> wenn Monster tot entferne es aus Liste, sonst losingscreen
while len(monsterList) > 0: 
    monster = monsterList[0]
    # Kampf simulieren
    # Wenn Monster tot -> entferne aus Liste
    # Wenn Monster nicht tot -> losingscreen
    monsterList.pop(0)