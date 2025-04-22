# Author: Sharif Wurz, Xiaoxuan Zhang
# This is a game to teach people the Dothraki numbers from 0 to 19.
import math
import random
from assets import GameDataLink

# Retrieving game data for collaboration
gameData = GameDataLink.get_data()
gameData["neededPoints"] = 5
gameData["text"] = "This game is about learning Dothraki numbers (from 0 to 19)."
gameData["earnedPoints"] = 0


# Checks if tkinter library is installed
try:
    import tkinter as tk
    from tkinter import messagebox
    # tkinter is installed
except ImportError:  # if tk not installed
    print("tkinter is not installed. Please install it to run this program.")
    print("Please install the tk library using the command 'pip install tk' and try again.")
    exit()  # exit


# Dothraki numbers from 0 to 19
dothrakiNumbers = {
    0: "som", 1: "at", 2: "akat", 3: "sen",
    4: "tor", 5: "mek", 6: "zhinda", 7: "fekh",
    8: "ori", 9: "qazat", 10: "thi", 11: "atthi",
    12: " akatthi", 13: "senthi", 14: " torthi", 15: "mekthi",
    16: " zhinthi", 17: "fekhthi", 18: "oritthi", 19: "qazathi"
}

class DothrakiNumberGame:
    def __init__(self, root):
        # Setting up window
        self.root = root
        self.root.title("Learning Dothraki Numbers")
        self.root.configure(bg="#696969")  # gray background

        # Defining fonts
        self.titleFont = ("Helvetica", 24, "bold")
        self.buttonFont = ("Helvetica", 16)
        self.scoreFont = ("Helvetica", 18, "italic")
        self.backgroudColor = "#696969"
        self.fontColor = "#141414"

        # Getting the screen width and height of the users display
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()

        # for the small windows (message boxes)
        self.smallWindowWidth = math.floor(self.screenWidth/3)
        self.smallWindowHeight = math.floor(self.screenHeight/3)

        # Setting the window size to 50% of the display metrics
        windowWidth = int(self.screenWidth * 0.5)
        windowHeight = int(self.screenHeight * 0.5)

        # Positioning the window in tahe center of the display
        self.positionX = int((self.screenWidth - windowWidth) / 2)
        self.positionY = int((self.screenHeight - windowHeight) / 2)

        # Setting the width, height and position of the window using the accorinding function
        # unfortunately, the function only takes a string
        self.root.geometry(f"{windowWidth}x{windowHeight}+{self.positionX}+{self.positionY}")

        # Init variables
        self.score = 0  # init score
        self.totalQuestions = 0  # init question count
        self.tries = 0 # init wrong tries

        # Title label
        self.titleLabel = tk.Label(root, text="Learn Dothraki Numbers", font=self.titleFont, bg=self.backgroudColor, fg=self.fontColor)
        self.titleLabel.pack(pady=20)

        # Question label
        self.questionLabel = tk.Label(root, text="", font=("Arial", 24), bg=self.backgroudColor, fg=self.fontColor)
        self.questionLabel.pack(pady=20)

        # Creating frame for the buttons
        self.buttonFrame = tk.Frame(root, bg=self.backgroudColor)
        self.buttonFrame.pack()

        # Init answer buttons
        self.answerButtons = []
        for i in range(4):  # 4 answer buttons
            button = tk.Button(self.buttonFrame, text="", font=("Arial", 16), width=10, height=2, command=lambda b=i: self.checkAnswer(b), activebackground="blue")
            if i < 2:
                button.grid(row=i, column=0, padx=10, pady=5)  # left two buttons
            else:
                button.grid(row=i-2, column=1, padx=10, pady=5)  # right two buttons
            self.answerButtons.append(button)

        # Initial score label
        self.scoreLabel = tk.Label(root, text="Score: 0/0", font=("Arial", 16), bg=self.backgroudColor, fg=self.fontColor)
        self.scoreLabel.pack(pady=20)

        self.generateQuestion() # generating first question

    # Generating the question
    def generateQuestion(self):
        if len(dothrakiNumbers) == 0:  # Check if all questions are answered
            self.questionLabel.config(text="The game is Over!\nYou've learned all numbers.")
            self.root.after(2000, self.root.destroy)
            return

        self.currentNumber = random.choice(list(dothrakiNumbers.keys()))  # Randomly selecting a number

        # Randomly selecting the question type chosen
        if random.random() < 0.5:  # 50% chance to ask English to Dothraki
            self.questionLabel.config(text=f"What is '{dothrakiNumbers[self.currentNumber]}' in English?")
            self.correctAnswer = str(self.currentNumber)
        else:  # 50% chance to ask Dothraki to English
            self.questionLabel.config(text=f"What is '{self.currentNumber}' in Dothraki?")
            self.correctAnswer = dothrakiNumbers[self.currentNumber]

        # Generate the four options
        options = [self.correctAnswer]

        # fallback if dictionary doesn't have enough unique unsed numbers left
        fallback = [str(num) for num in range(20)]

        while len(options) < 4:  # if there are less than 4 options

            # Randomly select a number from dictionary
            if len(dothrakiNumbers) >= 4:  # if there are enough unique numbers

                # if there are less than 3 correct answers
                if len(options) < (4 - (4 - max(3 - self.score // 3, 1))):
                    # Randomly select dothraki numbers
                    randomNumber = random.choice(list(dothrakiNumbers.keys()))
                    option = str(randomNumber)
                else:  # if there are more than 3 correct answers
                    randomNumber = random.choice(list(dothrakiNumbers.values())) # Randomly select english numbers
                    option = randomNumber
            else:
                # Use fallback if dictionary doesn't have enough unique unsed numbers
                option = random.choice(fallback)

            if option not in options:  # if option is not already in list
                options.append(option)  # add option to list

        random.shuffle(options)

        # Update button texts
        for i, button in enumerate(self.answerButtons):
            button.config(text=options[i])

    # Checking answers for correctness
    def checkAnswer(self, button_index):
        selectedAnswer = self.answerButtons[button_index].cget("text")

        if selectedAnswer == self.correctAnswer:  # if answer is correct

            if len(dothrakiNumbers) > 1:  # if there are more questions to follow
                self.showCorrectMessage()  # show correct message box/window

            self.score += 1 - self.tries  # increment score if no wrong try for this question
            self.totalQuestions += 1  # increment question count
            self.scoreLabel.config(text=f"Score: {self.score}/{self.totalQuestions}")

            if self.tries == 0:  # if no wrong tries for this question
                gameData["earnedPoints"] += 1  # increment earned points by 1

                # if minimum points are reached (5 points)
                if gameData["earnedPoints"] == gameData["neededPoints"]:
                    gameData["rewardText"] = "Great job! You've earned the minimum points needed." # set reward text
                    GameDataLink.send_data(gameData)  # send game data
                # remove the current number from dictionary for next questions
                dothrakiNumbers.pop(self.currentNumber, None)

                # Checking if dictionary is empty, if all questions are answered
                if len(dothrakiNumbers) == 0:
                    self.showWinningMessage()  # show winning message box/window
                    self.questionLabel.config(text="Game Over!\nYou learned all numbers.") 
                    # Quitting the game after 5 seconds
                    self.root.after(5000, self.root.destroy)
                    return
            self.tries = 0  # resetting wrong tries
            self.generateQuestion()  # moving to next question
        else:  # if answer is incorrect
            self.showIncorrectMessage()  # show incorrect message box/window
            self.tries = 1  # set wrong tries

    # Correct message box
    def showCorrectMessage(self):
        msgBox = tk.Toplevel(self.root)  # creating a new window
        msgBox.title("Correct!")  # set title to "Correct!"
        msgBox.geometry(f"{self.smallWindowWidth}x{self.smallWindowHeight}+{self.positionX+math.floor(self.smallWindowWidth/3.5)}+{self.positionY+math.floor(self.smallWindowHeight/3.5)}")  # setting window size and position
        tk.Label(msgBox, text="That's right!", font=self.titleFont, bg="#f0f0f0", fg="#00CC00").pack(pady=20) # green text, message set to "That's right!"
        self.root.after(1500, msgBox.destroy)  # close window after 1.5 seconds

    # Incorrect message box
    def showIncorrectMessage(self):
        msgBox = tk.Toplevel(self.root)  # creating a new window
        msgBox.title("Incorrect!")  # set title to "Incorrect!"
        msgBox.geometry(f"{self.smallWindowWidth}x{self.smallWindowHeight}+{self.positionX+math.floor(self.smallWindowWidth/3.5)}+{self.positionY+math.floor(self.smallWindowHeight/3.5)}")  # setting window size and position
        tk.Label(msgBox, text="Try again!", font=self.titleFont, bg="#f0f0f0", fg="#FF0000").pack(pady=20) # red text, message set to "Try again!"
        self.root.after(1500, msgBox.destroy)  # close window after 1.5 seconds

    # Winning message if all questions were answered correctly once
    def showWinningMessage(self):
        msgBox = tk.Toplevel(self.root)  # creating new window
        msgBox.title("You Won!")  # set title to "You Won!"
        msgBox.geometry(f"{self.smallWindowWidth}x{self.smallWindowHeight}+{self.positionX+math.floor(self.smallWindowWidth/3.5)}+{self.positionY+math.floor(self.smallWindowHeight/3.5)}")
        tk.Label(msgBox, text="You have answered\nall the questions!", font=self.titleFont, bg="#f0f0f0", fg="#00CC00").pack(pady=20) # green text, message set to "You have answered all the questions!"
        gameData["rewardText"] = "Well done! You have learned all the Dothraki numbers."
        GameDataLink.send_data(gameData)  # Send game data, as game was won
        self.root.after(1500, msgBox.destroy)  # close window after 1.5 seconds


if __name__ == "__main__":  # checks if code was called correctly
    root = tk.Tk()  # Init windows
    game = DothrakiNumberGame(root)  # Sets up window
    root.mainloop()  # starts game and runs until user closes window
