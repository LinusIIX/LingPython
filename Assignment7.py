# Assignment 7

# Luca Pomm, Linus Prange, Daniel Shaw, Nils Schiele

import random

## Helper functions
# wrapps input so x can always quit the program, r can always return to the selection menu, >
def inputQuittable(displayStr="", endStr="x", menuStr="r"):
  str = input(displayStr)
  if str == endStr:
    print("Goodbye see u soon")
    exit()
  if str == menuStr:
    sel()
  return str

# Ex.1)
def ex1():
  print("\n\t\tThis is a sentence generator.")
  choice = None
  while choice != "0":
    
    print(
    """
    x - Quit
    1 - return a random noun
    2 - return a random determiner
    3 - return a random adjective 
    4 - return a random transitive verb
    5 - return a random preposition
    6 - return a random noun phrase
    7 - return a random verb phrase
    8 - return a prepositional phrase
    9 - return a simple sentence 
    """
    )
    
    choice = inputQuittable("Choice: ")

    # else call up the various functions
    if choice == '1':
      print("You chose to generate a noun:  It is:\t", noun()) 

    elif choice == '2':
      print("You chose to generate a determiner:  It is:\t", det()) 

    elif choice == '3':
      print("You chose to generate an adjective  It is:\t", adj()) 

    elif choice == '4':
      print("You chose to generate a transitive verb:  It is:\t", verb()) 

    elif choice == '5':
      print("You chose to generate a preposition:  It is:\t", prep())

    elif choice == '6': 
      print("You chose to generate a noun phrase:  It is:\t", np())

    elif choice == '7':
      print("You chose to generate a verb phrase:  It is:\t", vp()) 

    elif choice == '8':
      print("You chose to generate a prepositional phrase:  It is:\t", pp())

    elif choice == '9':
      print("You chose to generate a sentence:  It is:\t", s()) 


    
# returns a random noun
def noun():
    """Return a random noun"""
    n = ['dog', 'cat', 'poodle', 'manx']
    return random.choice(n)
# returns a random determiner
def det():
    """Return a random determiner"""
    return random.choice(['a', 'the'])
# returns a random adjective
def adj():
    """Return a random adjective"""
    return random.choice(['sad', 'happy', 'silly'])
# returns a random transitive verb
def verb():
    """Return a transitive verb"""
    return random.choice(['likes', 'saw'])
# returns a random preposition
def prep(): 
    """Return a preposition"""
    return random.choice(['with', 'in', 'on', 'by'])
# returns a random noun phrase
def np():
    """Returns a random noun phrase"""
    return det() + ' ' + adj() + ' ' + noun()
# returns a random verb phrase
def vp():
    """Returns a random verb phrase"""
    return verb() +  ' ' + np()
# returns a prepositional phrase
def pp(): 
    """Returns a random prepositional phrase"""
    return prep() + ' ' + np()
# returns a simple sentence
def s():
    """Return a simple sentence"""
    return np().capitalize() + ' ' + vp() + '.'

# Ex.2)
def ex2():
  print("TODO")

# Ex.3)
def ex3():
  while True:
    make_word_count_dict(inputQuittable("Enter a file name to generate a word count dict.:"))

def make_word_count_dict(fileName):
  dict = {}
  # open the file into text as string and remove all new lines charachters
  file = open(fileName, "r")
  text = file.read()
  file.close()
  text = text.replace("\n", "")
  # split the text based on white space and go through all words add if it does not exist and count up when already there
  words = text.split(" ")
  for word in words:
    if word in dict:
      dict[word] += 1
    else:
      dict[word] = 1
  # open file to write the results change also fileName for easy handling
  fileName = fileName.replace(".", "_word_count.")
  file = open(fileName, "w")
  file.write(str(dict))
  file.close()


# setup for easy task selection
def sel():
  while True:
    # this function calling structure with Quittable can lead to a stack overflow but this is not that important here
     str = inputQuittable("Type 1-3 to view exercises\nType x in at any point to quit and r to return to exercise select\n")
     if str == "1": ex1()
     if str == "2": ex2()
     if str == "3": ex3()

# main, entry point of the program        
if __name__ == "__main__":
  sel()
