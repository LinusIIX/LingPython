# menu_state.py
# Author: Max Weber, Mojtaba Malek-Nejad
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

class MenuState:
    def __init__(self):
        # Menu states
        self.MAIN = "main"
        self.MODE = "mode"
        self.DIFFICULTY = "difficulty"
        self.ABOUT = "about"
        
        # Current state
        self.current_menu = self.MAIN
        
        # Game modes and difficulties
        self.modes = ["Strikes", "Endless", "Timed"]
        self.difficulties = ["Easy", "Normal", "Hard", "Insane"]
        
        # Selected and temporary selections
        self.selected_mode = "Strikes"
        self.selected_difficulty = "Normal"
        self.temp_mode = None
        self.temp_difficulty = None
    
    def switch_to_main(self):
        self.current_menu = self.MAIN
    
    def switch_to_mode(self):
        self.current_menu = self.MODE
        self.temp_mode = self.selected_mode
    
    def switch_to_difficulty(self):
        self.current_menu = self.DIFFICULTY
        self.temp_difficulty = self.selected_difficulty
    
    def switch_to_about(self):
        self.current_menu = self.ABOUT
    
    def apply_mode(self):
        if self.temp_mode:
            self.selected_mode = self.temp_mode
        self.switch_to_main()
    
    def apply_difficulty(self):
        if self.temp_difficulty:
            self.selected_difficulty = self.temp_difficulty
        self.switch_to_main()
    
    def cancel_selection(self):
        self.temp_mode = None
        self.temp_difficulty = None
        self.switch_to_main()
    
    def select_mode(self, mode):
        if mode in self.modes:
            self.temp_mode = mode
    
    def select_difficulty(self, difficulty):
        if difficulty in self.difficulties:
            self.temp_difficulty = difficulty
    
    def get_current_menu(self):
        return self.current_menu
    
    def get_selected_mode(self):
        return self.selected_mode
    
    def get_selected_difficulty(self):
        return self.selected_difficulty 