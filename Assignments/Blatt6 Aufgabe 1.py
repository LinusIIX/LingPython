Dictionary = {  
    "Allegory": "An allegory is an extended metaphor, especially a story in which fictional characters and actions are used to understand and express aspects of concepts relating to human existence.",
    "Adjective": "An adjective is a word that belongs to a class whose members modify nouns. An adjective specifies the properties or attributes of a noun referent.",
    "Anthimeria": "Anthimeria is the use of a member of one word class as if it were a member of another, thus altering its meaning.",
    "Valency": "Valency refers to the capacity of a verb to take a specific number and type of arguments (noun phrase positions).",
    "Syllable": "A syllable is a unit of sound composed of a central peak of sonority (usually a vowel), and the consonants that cluster around this central peak.",
    "Substantive": "A substantive is a broad classification of words that includes nouns and nominals."
}

def print_dictionary():
    for key in Dictionary:
        print(key)

def look_up(word):
    if word in Dictionary:
        print(Dictionary[word])
    else:
        print("The word is not in the dictionary.")

def add_word(word, definition):
    Dictionary[word] = definition
    print("The word has been added to the dictionary.")

def main():

    print("Welcome to the dictionary.")
    print("The words in the dictionary are: ")
    print_dictionary()

    print("Options:")
    print("1. Look up a term (press 1)")
    print("2. Add a term (press 2)")
    print("3. Quit (press 3)")

    while True:
        user_input = input("What do you want to do: ")  
        if user_input in ["1", "2", "3"]:
            if user_input == "1":
                word = input("Enter the word you want to search: ")
                look_up(word)
            elif user_input == "2":
                word = input("Enter the word you want to add: ")
                definition = input("Enter the definition of the word: ")
                add_word(word, definition)
            elif user_input == "3":
                print("Thank you for using the dictionary.")
                break
        else:
            print("Invalid input. Please try again.")


# Run the program
if __name__ == "__main__":
    main()
