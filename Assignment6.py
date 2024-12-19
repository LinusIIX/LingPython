## Helper functions

# wrapps input so x can always quit the program, r can always return to the selection menu, and the input is returned
def inputQuittable(displayStr="", endStr="x", menuStr="r"):
  str = input(displayStr)
  if str == endStr:
    print("Goodbye see u soon")
    exit()
  if str == menuStr:
    sel()
  return str


# Ex.1)
# Handles different cases of searching or adding terms and first looks if the term is in lingTerms as other wise an access error can happen.
# Same for adding here only new terms can be added so the cant be in lingTerms. (inputQuittable is used in all exercises to make all input quittable and allow to end with x at all points)
lingTerms = {  
    "Allegory": "An allegory is an extended metaphor, especially a story in which fictional characters and actions are used to understand and express aspects of concepts relating to human existence.",
    "Adjective": "An adjective is a word that belongs to a class whose members modify nouns. An adjective specifies the properties or attributes of a noun referent.",
    "Anthimeria": "Anthimeria is the use of a member of one word class as if it were a member of another, thus altering its meaning.",
    "Valency": "Valency refers to the capacity of a verb to take a specific number and type of arguments (noun phrase positions).",
    "Syllable": "A syllable is a unit of sound composed of a central peak of sonority (usually a vowel), and the consonants that cluster around this central peak.",
    "Substantive": "A substantive is a broad classification of words that includes nouns and nominals."
}
def ex1():
  while True:
    inStr = inputQuittable("type 1 to look up a term and 2 to add another term\n")
    #inStr == "3" is not necessary as the inputQuittable function takes care of this
    if inStr == "1":
      inStr = inputQuittable("search term:\n")
      description = "term does not exist"
      #only if the term exists get the description if not the "term does not exist" string says and gets printed
      if inStr in lingTerms:
        description = lingTerms[inStr]
      print(inStr, " : ", description)
    if inStr == "2":
      inStr = inputQuittable("add a new term:\n")
    #if already defined retry
    if inStr in lingTerms:
      print("term is already defined")
      continue
    lingTerms[inStr] = inputQuittable("add a description to you term:\n")

#Ex.2)
# We get the keys of the first dict and then iterate over them so we can access each key on both dicts easy.
# Then we add them into dict1 and print (this can be done with n dicts easily)
def ex2():
  dict1 = {"Harry": 3, "the": 8, "laugh": 3}
  dict2 = {"Harry": 4, "the": 6, "laugh": 1}
  for key in dict1.keys():
    dict1[key] += dict2[key]
    print(dict1[key])

#Ex.3)
# There is a dictionary with words and their syllables and we can look up the syllables of a word and get the count of words with a certain syllable count
Dictionarie_Syllables = {
    "banana": 3,
    "apple": 2,
    "orange": 2,
    "strawberry": 3,
    "grape": 1,
    "watermelon": 4,
    "blueberry": 3,
    "kiwi": 2,
    "pineapple": 3,
    "mango": 2
}
# Create a dictionary where the key is the syllable count and the value is the number of words with that syllable count
def create_syllable_count_dict():
    syllable_count_dict = {}
    for word, syllables in Dictionarie_Syllables.items():
        if syllables in syllable_count_dict:
            syllable_count_dict[syllables] += 1
        else:
            syllable_count_dict[syllables] = 1
    return syllable_count_dict

# Function to look up the syllable count of a word
def lookup_word(word):
    return Dictionarie_Syllables.get(word, "Word not found in dictionary")

# Function to find out how many words have a certain number of syllables
def words_with_syllables(syllable_count):
    syllable_count_dict = create_syllable_count_dict()
    return syllable_count_dict.get(syllable_count, 0)

# User interaction
def ex3():
  while True:
      print("There are 10 words in our dictionary. Each word has a certain number of syllables.")
      print("Options:")
      print("1. Look up a word")
      print("2. Find out how many words have a certain number of syllables")
      print("x Exit")
      choice = inputQuittable("Enter your choice: ")
      #when the input is "1" or "2" print and call the function for this option, x leads through inputQuittable to exit
      if choice == "1":
          word = inputQuittable("Enter a word: ")
          print(f"The word '{word}' has {lookup_word(word)} syllables.")
      elif choice == "2":
          syllable_count = int(inputQuittable("Enter a number of syllables: "))
          print(f"There are {words_with_syllables(syllable_count)} words which consist of {syllable_count} syllables in our dictionary.")
      else:
          print("Invalid choice. Please try again.")

#Ex.4)
# Impl. function according to (link) and calling it in a loop while True is okay as we use inputQuittable()
def celsius_to_fahrenheit(celsius):
  return (celsius / 5) * 9 + 32

def ex4():
  while True:
    str = inputQuittable("Get Fahrenheit from a number in celsius:\n")
    #Calling c_to_f with string as number converted through int()
    print(int(str), "celsius is", celsius_to_fahrenheit(int(str)), "in fahrenheit")

#Ex.5)
# Opens file (it has to exist) reads it then gets all words once and sorts them then we get all words lowercase and add them to one string that we write out as lowerWords.txt
def ex5():
  str = inputQuittable("type the name of a file to open (it has to be in the same directory as where the python script is executed)\n")
  file = open(str, "r")
  text = file.read()
  file.close()
  words = text.split(" ")
  words.sort()
  print(words)
  
  #accumulate all words in a string and write it to a new file
  outText = ""
  for word in words:
    if word == word.lower():
     outText += word + "\n"
  file = open("lowerWords.txt", "w")
  file.write(outText)
  file.close()

#Setup for easy task selection
def sel():
  while True:
    #This function calling structure with Quittable can lead to a stack overflow but this is not that important here
    sel = inputQuittable("Type 1-5 to view exercises\nType x in at any point to quit and r to return to exercise select\n")
    match sel:
      case "1": ex1()
      case "2": ex2()
      case "3": ex3()
      case "4": ex4()
      case "5": ex5()

# main, entry point of the program        
if __name__ == "__main__":
  sel()
