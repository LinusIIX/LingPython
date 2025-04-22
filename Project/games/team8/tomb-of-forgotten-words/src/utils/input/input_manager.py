import pygame


class InputManager:
    """
    Manages keyboard and mouse input for the game using a singleton pattern.

    Attributes:
        m_key_pressed (dict[int, bool]): Dictionary to track the state of keys (pressed or not).
        m_key_action (dict[int, callable]): Dictionary to map keys to their respective functions.
        m_button_pressed (dict[int, bool]): Dictionary to track the state of mouse buttons (pressed or not).
        m_button_action (dict[int, callable]): Dictionary to map mouse buttons to their respective functions.
        m_scroll_action (callable): Function to call when the mouse scroll is used.
        m_camera (pygame.Rect): Camera viewport to calculate the world mouse position.
    """

    _instance = None  # static variable, to hold instance for singleton pattern

    def __new__(cls):
        """
        Ensures that only one instance of InputManager is created (singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.m_initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the InputManager instance.

        Prevents re-initialization to avoid clearing the dictionaries.
        """
        if self.m_initialized:  # prevent re-initialization, which causes the dictionaries to clear
            return
        self.m_initialized = True
        # keyboard input
        self.m_key_pressed: dict[int, bool] = {}  # dictionary for key pressed booleans
        self.m_key_action: dict[int, callable] = {}  # dictionary for key press functions

        # mouse input
        self.m_button_pressed: dict[int, bool] = {}  # dictionary for button pressed booleans
        self.m_button_action: dict[int, callable] = {}  # dictionary for button press functions
        self.m_scroll_action: callable = None

        self.m_camera: pygame.Rect = None  # camera viewport to calculate the world mouse pos

    def is_key_pressed(self, key_code: int) -> bool:
        """
        Checks if a key is pressed down.

        Args:
            key_code (int): The key code to check.

        Returns:
            bool: True if the key is pressed, False otherwise.
        """
        return (key_code in self.m_key_pressed) and self.m_key_pressed[key_code]

    def is_button_pressed(self, button: int) -> bool:
        """
        Checks if a mouse button is pressed down.

        Args:
            button (int): The mouse button to check.

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return (button in self.m_button_pressed) and self.m_button_pressed[button]

    # Keyboard Input ###################################
    def press_key(self, key_code: int) -> None:
        """
        Marks a key as pressed and calls its assigned function if any.

        Args:
            key_code (int): The key code to press.
        """
        self.m_key_pressed[key_code] = True
        if key_code in self.m_key_action:
            self.m_key_action[key_code]()

    def release_key(self, key_code: int) -> None:
        """
        Marks a key as released.

        Args:
            key_code (int): The key code to release.
        """
        self.m_key_pressed[key_code] = False

    def assign_function_to_key(self, key_code: int, function: callable) -> None:
        """
        Assigns a function to be called when a key is pressed.

        Args:
            key_code (int): The key code to assign the function to.
            function (callable): The function to call when the key is pressed.
        """
        self.m_key_action[key_code] = function

    def remove_key_function(self, key_code: int) -> None:
        """
        Removes the assigned function from a key.

        Args:
            key_code (int): The key code to remove the function from.
        """
        if key_code in self.m_key_action:
            self.m_key_action.pop(key_code)

    def clear_key_functions(self) -> None:
        """
        Clears functions of all keys.
        """
        self.m_key_action.clear()

    # Mouse Input ######################################
    def press_mb(self, btn: int) -> None:
        """
        Marks a mouse button as pressed and calls its assigned function if any.

        Args:
            btn (int): The mouse button to press.
        """
        self.m_button_pressed[btn] = True
        if btn in self.m_button_action:
            self.m_button_action[btn]()

    def release_mb(self, btn: int) -> None:
        """
        Marks a mouse button as released.

        Args:
            btn (int): The mouse button to release.
        """
        self.m_button_pressed[btn] = False

    def scroll(self, direction: int) -> None:
        """
        Calls the assigned scroll function with the scroll direction.

        Args:
            direction (int): The scroll direction.
        """
        if self.m_scroll_action is not None:
            self.m_scroll_action(direction)

    def assign_function_to_mouse_button(self, btn: int, function: callable) -> None:
        """
        Assigns a function to be called when a mouse button is pressed.

        Args:
            btn (int): The mouse button to assign the function to.
            function (callable): The function to call when the button is pressed.
        """
        self.m_button_action[btn] = function

    def assign_function_to_scroll(self, function: callable) -> None:
        """
        Assigns a function to be called when the mouse is scrolled.

        Args:
            function (callable): The function to call when the mouse is scrolled.
        """
        self.m_scroll_action = function

    def remove_button_function(self, btn: int) -> None:
        """
        Removes the assigned function from a mouse button.

        Args:
            btn (int): The mouse button to remove the function from.
        """
        if btn in self.m_button_action:
            self.m_button_action.pop(btn)

    def remove_scroll_functions(self) -> None:
        """
        Removes the assigned scroll function.
        """
        self.m_scroll_action = None

    def get_mouse_screen_pos(self) -> tuple[int, int]:
        """
        Gets the current mouse position on the screen.

        Returns:
            tuple[int, int]: The current mouse position (x, y).
        """
        return pygame.mouse.get_pos()

    def get_mouse_world_pos(self) -> tuple[int, int]:
        """
        Gets the current mouse position in the world, adjusted by the camera viewport.

        Returns:
            tuple[int, int]: The current mouse position in the world (x, y).
        """
        screen_pos = self.get_mouse_screen_pos()
        return (screen_pos[0] + self.m_camera.left, screen_pos[1] + self.m_camera.top)

    def set_camera(self, camera_rect: pygame.Rect) -> None:
        """
        Sets the camera viewport for calculating the world mouse position.

        Args:
            camera_rect (pygame.Rect): The camera viewport rectangle.
        """
        self.m_camera = camera_rect

    def get_button_function(self, button: int) -> callable:
        """
        Gets the assigned function for a mouse button.

        Args:
            button (int): The mouse button to get the function for.

        Returns:
            callable: The assigned function or a default function if none is assigned.
        """
        if button in self.m_button_action:
            return self.m_button_action[button]
        return lambda: print("no function assigned!")
