import os, pygame


class AssetManager:
    """
    Singleton class that manages game assets including images, music, and sound effects.
    """

    _instance = None  # static instance for singleton pattern

    def __new__(cls):  # constructor to return singleton instance
        if cls._instance is None:  # if the instance doesn't exist one shall be created
            cls._instance = super().__new__(cls)
            cls._instance.m_initialized = False  # prevent accidental re-initialization
        return cls._instance

    def __init__(self):
        """
        Initializes the AssetManager.

        Sets up directories and dictionaries for images, music, and sound effects.
        """
        if self.m_initialized:  # check that the instance has not been initialized yet
            return  # if it has do nothing
        self.m_initialized = True  # if not mark it as initialized and proceed as usual
        self.m_img_dir = "img"
        self.m_sfx_dir = "sfx"
        self.m_audio_dir = "audio"
        self.m_music_dir = "music"
        self.m_assets_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")
        )
        self.m_images: dict[str, pygame.Surface] = {}
        self.m_music: dict[str, pygame.mixer.Sound] = {}
        self.m_sfx: dict[str, pygame.mixer.Sound] = {}

    def load_images(self, update_callback=None) -> None:
        """
        Loads all images from the assets img folder into the images dictionary.

        Args:
            update_callback (callable, optional): Function to call to update the loading progress.
        """
        folder_path = os.path.join(self.m_assets_path, self.m_img_dir)  # get the img folder path
        if not os.path.isdir(folder_path):  # check that the folder exists
            raise FileNotFoundError(f"Image folder not found: {folder_path}")

        files = [
            file for file in os.listdir(folder_path) if file.endswith(".png")
        ]  # put all png files in img folder into a list
        total_files = len(files)  # get the count of all png files in img
        for i, file in enumerate(files):  # iterate through the list with i as a counter
            path = os.path.join(folder_path, file)  # get path to image file
            image = pygame.image.load(path).convert_alpha()  # load image file
            image_key = os.path.splitext(file)[
                0
            ]  # create a key for the dictionary by using the filename minus .png
            self.m_images[image_key] = image  # add the image to the dictionary
            if update_callback:  # if a callback function is provided
                update_callback(
                    (i + 1) / total_files
                )  # call it and tell how many of the images have been loaded

    def load_music(self, update_callback=None) -> None:
        """
        Loads all music files from the assets music folder into the music dictionary.

        Args:
            update_callback (callable, optional): Function to call to update the loading progress.
        """
        self.load_audio(self.m_music, self.m_music_dir, update_callback)

    def load_sfx(self, update_callback=None) -> None:
        """
        Loads all sound effect files from the assets sfx folder into the sfx dictionary.

        Args:
            update_callback (callable, optional): Function to call to update the loading progress.
        """
        self.load_audio(self.m_sfx, self.m_sfx_dir, update_callback)

    def load_audio(
        self, dictionary: dict[str, pygame.mixer.Sound], subdir: str, update_callback=None
    ) -> None:
        """
        Loads all ogg files from the specified audio subdirectory into the given dictionary.

        Args:
            dictionary (dict[str, pygame.mixer.Sound]): The dictionary to load audio files into.
            subdir (str): The subdirectory within the audio directory to load files from.
            update_callback (callable, optional): Function to call to update the loading progress.
        """
        folder_path = os.path.join(
            self.m_assets_path, self.m_audio_dir, subdir
        )  # get the audio subdirectory path
        if not os.path.isdir(folder_path):  # check that the folder exists
            raise FileNotFoundError(f"Audio folder not found: {folder_path}")

        files = [
            file for file in os.listdir(folder_path) if file.endswith(".ogg")
        ]  # put all ogg files in the subdirectory into a list
        total_files = len(files)  # get the count of all ogg files in the subdirectory
        for i, file in enumerate(files):  # iterate through the list with i as a counter
            path = os.path.join(folder_path, file)  # get path to audio file
            sound = pygame.mixer.Sound(path)  # load audio file
            audio_key = os.path.splitext(file)[
                0
            ]  # create a key for the dictionary by using the filename minus .ogg
            dictionary[audio_key] = sound  # add the sound to the dictionary
            if update_callback:  # if a callback function is provided
                update_callback(
                    (i + 1) / total_files
                )  # call it and tell how many of the audio files have been loaded

    def get_image(self, name: str) -> pygame.Surface:
        """
        Retrieves an image by name from the images dictionary.

        Args:
            name (str): The name of the image to retrieve.

        Returns:
            pygame.Surface: The image surface.

        Raises:
            KeyError: If the image does not exist.
        """
        if name not in self.m_images:
            raise KeyError(f"Image '{name}' does not exist!")
        return self.m_images[name]

    def get_image_scaled(self, name: str, size: tuple[int, int]) -> pygame.Surface:
        """
        Retrieves an image by name from the images dictionary and scales it to the specified size.

        Args:
            name (str): The name of the image to retrieve.
            size (tuple[int, int]): The desired size of the image.

        Returns:
            pygame.Surface: The scaled image surface.
        """
        return pygame.transform.scale(self.get_image(name), size)

    def get_image_rotated(self, name: str, angle: float) -> pygame.Surface:
        """
        Retrieves an image by name from the images dictionary and rotates it by the specified angle.

        Args:
            name (str): The name of the image to retrieve.
            angle (float): The angle to rotate the image.

        Returns:
            pygame.Surface: The rotated image surface.
        """
        return pygame.transform.rotate(self.get_image(name), angle)

    def get_music(self, name: str) -> pygame.mixer.Sound:
        """
        Retrieves a music track by name from the music dictionary.

        Args:
            name (str): The name of the music track to retrieve.

        Returns:
            pygame.mixer.Sound: The music track.

        Raises:
            KeyError: If the music track does not exist.
        """
        if name not in self.m_music:
            raise KeyError(f"Audio File '{name}' does not exist!")
        return self.m_music[name]

    def get_music_tracks(self, track_list: list[str]) -> list[pygame.mixer.Sound]:
        """
        Retrieves a list of music tracks by their names from the music dictionary.

        Args:
            track_list (list[str]): The list of music track names to retrieve.

        Returns:
            list[pygame.mixer.Sound]: The list of music tracks.
        """
        tracks: list[pygame.mixer.Sound] = []
        for track in track_list:
            tracks.append(self.get_music(track))
        return tracks

    def get_sound_effect(self, name: str) -> pygame.mixer.Sound:
        """
        Retrieves a sound effect by name from the sfx dictionary.

        Args:
            name (str): The name of the sound effect to retrieve.

        Returns:
            pygame.mixer.Sound: The sound effect.

        Raises:
            KeyError: If the sound effect does not exist.
        """
        if name not in self.m_sfx:
            raise KeyError(f"Audio File '{name}' does not exist!")
        return self.m_sfx[name]

    def set_sfx_volume(self, volume: float) -> None:
        """
        Sets the volume for all sound effects.

        Args:
            volume (float): The volume level (0.0 to 1.0).

        Raises:
            ValueError: If the volume is not within the valid range.
        """
        if volume < 0 or volume > 1:
            raise ValueError(f"Error: {volume} is not a valid volume value!")
        for sound_name, sound in self.m_sfx.items():
            sound.set_volume(volume)
