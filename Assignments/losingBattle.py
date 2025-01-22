# Losing Battle fixed
# Demonstrates the dreaded infinite loop
import random

print("Your lone hero is surrounded by a massive army of trolls.")
print("Their decaying green bodies stretch out, melting into the horizon.")
print("Your hero unsheathes his sword for the last fight of his life.\n")

#Variables defining the game
health = 10
enemyCounter = 0
trollDamage = 3
ogreDamage = 1
witchHeal = 0
armySize = 100000

#The game goes on as long as there are enemies to slay or health left
while health > 0 and enemyCounter < armySize: # edit != to < so program does not produce an infinite loop
    #Witch heal is applied after the last round a reward for winning
    if witchHeal > 0:
        print("You freed a witch and get", witchHeal, "healing.")
        health += witchHeal
        print("You health is now:", health)
    print("Two groups approach which to attack?")

    #Here the two options are randomly generated number of enemies and amount of heal for each side
    #Also the ranges get bigger as the game progresses determind by the number of enemies slayn
    lTrolls = random.randint(0, 3)
    rTrolls = random.randint(0, 3)
    lOgres = random.randint(0, enemyCounter//2 + 1)
    rOgres = random.randint(0, enemyCounter//2 + 1)
    lWitch = random.randint(3, enemyCounter//2 + 5)
    rWitch = random.randint(3, enemyCounter//2 + 5)
    #Tell the user what are the two options
    print("On the left you see", lTrolls, "Trolls and", lOgres, "Ogres.")
    print("On the right there are", rTrolls, "Trolls and", rOgres, "Ogres.")
    print("Both hold a witch hostage the left one will heal", lWitch , "and the right", rWitch, ".")
    
    #Capture and evaluate input then apply damage
    command = input("What do you do? type [left] or [right]:")
    if command == "left":
        damage = trollDamage * lTrolls + ogreDamage * lOgres
        enemyCounter += lTrolls + lOgres
        witchHeal = lWitch
    else:
        damage = trollDamage * rTrolls + ogreDamage * rOgres
        enemyCounter += rTrolls + rOgres
        witchHeal = rWitch
    health -= damage

    print("Your hero swings and defeats the enemies." \
          "but takes", damage, "damage points.\n")

#When the game ends our hero won or was defeated, check through the health
if health < 0:
    print("Your hero fought valiantly and defeated", enemyCounter, "enemies.")
    print("But alas, your hero is no more.")
else:
    print("Congratulation you fought all enemies of.\nThe enemies pile high to the sky with", enemyCounter, "piled on above the other.")

input("\n\nPress the enter key to exit.")
