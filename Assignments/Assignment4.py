# Python Lesson 4
# Luca Pomm, Nils Schiele, Linus Prange, Daniel Shaw


#------------------------------------------------------------
# Exercise 1
# Ask the user for a string that has at least 5 characters, slice the first 2 characters and add them to the end of the string

# Ask the user for a string that has at least 5 characters 
string = input("Enter a string that has at least 5 characters: ")

# if the user input is not acceptable, ask for another input
while len(string) < 5:
    string = input("The Input is not acceptable. Enter a string that has at least 5 characters: ")

# store the first 2 characters in a temporary string
temp_string = string[:2]
# remove the first 2 characters from the string
string = string[2:]
# add the temporary string to the end of the string
string = string + temp_string
print(string)


#------------------------------------------------------------
# Exercise 2
# Ask the user for a message and remove all voiced consonants from the message

message = input("Enter a message: ")
new_message = ""
VOICED_CONSONANTS = "bdgjlmnrvwyz"

message = message.replace("tH", "")
message = message.replace("sZ", "")
message = message.replace("th", "")
message = message.replace("sz", "")
message = message.replace("Th", "")
message = message.replace("Sz", "")
message = message.replace("TH", "")
message = message.replace("SZ", "")

# Check each letter if it is a voiced consonant, otherwise add it to the new message
for letter in message:
    if letter.lower() not in VOICED_CONSONANTS:
        new_message += letter

# Output
print("Your message without voiced consonants is:", new_message)
print()


#------------------------------------------------------------
# Exercise 3
# Ask the user for their name, an item they are carrying, and a magic word. If the name is Gandalf or the item is a magic wand, the gate will open. Otherwise, the magic word must contain both an "o" and the sequence "ld".

print("You and your companions stand before a great, ancient gate, its massive wings firmly shut. Suddenly, a voice echoes, deep and resonant, as if the stone itself were speaking:")
name = input("'Who dares to approach this threshold? Speak, travelers, or turn back and seek your fortune elsewhere!' ")
item = input(name + ", what are you carrying with you? ")
magic_word = input("Now tell me, " + name + ", with the " + item + ", what is the magic word to open the gate? ")

# Check if the gate will open
door = False
if name == "Gandalf" or item == "magic wand":
    door = True
else:
    # Check if the magic word contains both an "o" and the sequence "ld"
    if "o" in magic_word and "ld" in magic_word:
        door = True

# Output
if door:
    print("The gate slowly creaks open, and you step through, ready to face whatever lies beyond.")
    print()
else:
    print("The gate remains closed. The voice speaks once more:" + "'The way is barred. It was made by those who are dead, and the dead keep it.'")
    print()

    
#------------------------------------------------------------
# Exercise 4
# Take a word from the user and translate it into robbers language

# Ask the user for a word
word = input("Enter a word: ")

# Create a new string to store the translated word
new_word = ""

# Loop through each letter in the word
for letter in word:
    # If the letter is a vowel, add it to the new word
    if letter.lower() in "aeiou":
        new_word += letter
    # If the letter is a consonant, add the letter followed by "o" and the letter again
    else:
        new_word += letter + "o" + letter

print("The word in robbers language is:", new_word)
#------------------------------------------------------------