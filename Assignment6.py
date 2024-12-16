## Helper functions

# wrapps input so x can always quit the program
def inputQuittable(displayStr="", endStr="x", menuStr="r"):
  str = input(displayStr)
  if str == endStr:
    print("Goodbye see u sone")
    exit()
  if str == menuStr:
    sel()
  return str


# Ex.1)
# Handles different cases of searching or adding terms and first looks if the term is in lingTerms as other wise an access error can happe.
# Same for adding here only new terms can be added so the cant be in lingTerms. (inputQuittable is used in all exercises to make all input quittable and allow to end with x at all points)
#TODO add 6 terms
lingTerms = {
  "term" : "definition"
}

def ex1():
  while True:
    inStr = inputQuittable("type 1 to look up a term and 2 to add another term\n")
    if inStr == "1":
      inStr = inputQuittable("search term:\n")
      description = "term does not exist"
      if inStr in lingTerms:
        description = lingTerms[inStr]
      print(inStr, " : ", description)
    if inStr == "2":
      inStr = inputQuittable("add a new term:\n")
    if inStr in lingTerms:
      print("term is already defined")
      continue
    lingTerms[inStr] = inputQuittable("add a description to you term:\n")

#Ex.2)
# We get the keys of the first dict and then itterat over them so we can access each key on both dicts easy.
# Then we add them into dict1 and print (this can be done with n dicts easily)
def ex2():
  dict1 = {"Harry": 3, "the": 8, "laugh": 3}
  dict2 = {"Harry": 4, "the": 6, "laugh": 1}
  for key in dict1.keys():
    dict1[key] += dict2[key]
    print(dict1[key])

#Ex.3)
def ex3():
  print("TODO")

#Ex.4)
# Impl. function according to (link) and calling it in a loop while True is okay as we use inputQuittable()
def celsius_to_fahrenheit(celsius):
  return (celsius / 5) * 9 + 32

def ex4():
  while True:
    str = inputQuittable("Get Fahrenheit from a number in celsius:\n")
    print(int(str), "celsius is", celsius_to_fahrenheit(int(str)), "in fahrenheit")

#Ex.5)
# Opens file (it has to exist) reads it then gets all words once and sorts them then we get all words lowercase and add them to one string that we write out as lowerWords.txt
def ex5():
  str = inputQuittable("type the name of a file to open (it has to be in the same directory as where the python script is executed)\n")
  file = open(str, "r")
  text = file.read()
  file.close()
  #Remove duplicates TODO ist das nötig?
  words = list(set(text.split(" ")))
  words.sort()
  print(words)

  outText = ""
  for word in words:
    if word == word.lower():
     outText += word + "\n"
  file = open("lowerWords.txt", "w")
  file.write(outText)
  file.close()

##Setup for easy task selection
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
sel()
