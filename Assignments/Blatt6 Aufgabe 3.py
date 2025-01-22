#--------------------------------------------------------------
# Exercise 3

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
while True:
    print("\nOptions:")
    print("1. Look up a word")
    print("2. Find out how many words have a certain number of syllables")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        word = input("Enter a word: ")
        print(f"The word '{word}' has {lookup_word(word)} syllables.")
    elif choice == "2":
        syllable_count = int(input("Enter a number of syllables: "))
        print(f"There are {words_with_syllables(syllable_count)} words which consist of {syllable_count} syllables in our dictionary.")
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")
#--------------------------------------------------------------