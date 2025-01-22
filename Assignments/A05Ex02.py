import random
nouns = ("Kopf", "Baum", "Pflanze", "Katze", "Hund", "Fortnite", "Sonne", "Tonne", "Berg", "Topf", "Wasser", "Hahn", "Huhn", "Kraut", "Schlauch")
adjective = ("rot", "blau", "feucht", "hell", "hart", "leicht", "voll", "hoch", "interaktiv")

inStr = ""

print("to quit the program type quit")
while inStr != "quit":
  if inStr != "":
    additionalWord = ""
    if inStr[0].isupper():
      idx = random.randint(0, len(adjective)-1)
      additionalWord = adjective[idx]
      print(additionalWord + inStr.lower())
    else:
      idx = random.randint(0, len(nouns)-1)
      additionalWord = nouns[idx]
      print(inStr + additionalWord.lower())
  inStr = input("type a noun or an adjective (nouns are starting with a capital letter):")
