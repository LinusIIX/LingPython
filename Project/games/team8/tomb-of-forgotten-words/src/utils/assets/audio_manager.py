import pygame
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.music_player import MusicPlayer


class AudioManager:
    """
    Singleton class that manages audio assets including sound effects and music.
    """

    _instance = None  # static instance for singleton pattern

    def __new__(cls):  # constructor to return singleton instance
        if cls._instance is None:  # if the instance doesn't exist one shall be created
            cls._instance = super().__new__(cls)
            cls._instance.m_initialized = False  # prevent accidental re-initialization
        return cls._instance

    @property
    def master_volume(self) -> float:
        """
        Returns the master volume level.

        Returns:
            float: The master volume level.
        """
        return self.m_master_volume

    @property
    def sfx_volume(self) -> float:
        """
        Returns the sound effects volume level.

        Returns:
            float: The sound effects volume level.
        """
        return self.m_sfx_volume

    @property
    def music_volume(self) -> float:
        """
        Returns the music volume level.

        Returns:
            float: The music volume level.
        """
        return self.m_music_volume

    def __init__(self):
        """
        Initializes the AudioManager instance.

        Sets up the audio mixer, loads assets, and initializes volume levels.
        """
        if self.m_initialized:  # check that the instance has not been initialized yet
            return  # if it has do nothing
        self.m_initialized = True  # if not mark it as initialized and proceed as usual

        pygame.mixer.init()
        pygame.mixer.set_num_channels(len(assets.MUSIC_LIST) + 16)
        self.m_master_volume: float = 1.0
        self.m_sfx_volume: float = 0.8
        self.m_music_volume: float = 1.0
        self.m_assets = AssetManager()
        self.m_music = MusicPlayer(
            self.m_assets.get_music_tracks(assets.MUSIC_LIST), fade_speed=0.01
        )
        self.m_active_tracks: set[int] = {0}

        self.apply_music_volume()
        self.apply_sfx_volume()

    def update(self):
        """
        Updates the music player.
        """
        self.m_music.update()

    def set_master_volume(self, volume: float) -> None:
        """
        Sets the master volume level.

        Args:
            volume (float): The new master volume level (0.0 to 1.0).
        """
        if 0 <= volume <= 1:
            self.m_master_volume = volume
            self.apply_sfx_volume()
            self.apply_music_volume()

    def set_sfx_volume(self, volume: float) -> None:
        """
        Sets the sound effects volume level.

        Args:
            volume (float): The new sound effects volume level (0.0 to 1.0).
        """
        if 0 <= volume <= 1:
            self.m_sfx_volume = volume
            self.apply_sfx_volume()

    def apply_sfx_volume(self) -> None:
        """
        Applies the sound effects volume level to all sound effects.
        """
        self.m_assets.set_sfx_volume(self.m_sfx_volume * self.m_master_volume)

    def set_music_volume(self, volume: float) -> None:
        """
        Sets the music volume level.

        Args:
            volume (float): The new music volume level (0.0 to 1.0).
        """
        if 0 <= volume <= 1:
            self.m_music_volume = volume
            self.apply_music_volume()

    def apply_music_volume(self) -> None:
        """
        Applies the music volume level to the music player.
        """
        self.m_music.set_master_volume(self.m_music_volume * self.m_master_volume)

    def play_sfx(self, sound_effect: str) -> None:
        """
        Plays a sound effect.

        Args:
            sound_effect (str): The name of the sound effect to play.
        """
        sound = self.m_assets.get_sound_effect(sound_effect)
        sound.play()

    def start_track(self, track: int) -> None:
        """
        Starts playing a single music track and fades it in.

        Args:
            track (int): The index of the track to start.
        """
        self.m_active_tracks.add(track)
        self.m_music.start_track(track)
        self.m_music.fade_in(track)

    def start_tracks(self, tracks: list[int]) -> None:
        """
        Starts playing multiple music tracks and fades them in.

        Args:
            tracks (list[int]): The list of track indices to start.
        """
        for i in tracks:
            self.m_active_tracks.add(i)
        self.m_music.start_multiple_tracks(tracks)
        self.m_music.fade_in_multiple(tracks)

    def stop_track(self, track: int) -> None:
        """
        Stops playing a single music track.

        Args:
            track (int): The index of the track to stop.
        """
        self.m_active_tracks.discard(track)
        self.m_music.stop_track(track)

    def stop_tracks(self, tracks: list[int]) -> None:
        """
        Stops playing multiple music tracks.

        Args:
            tracks (list[int]): The list of track indices to stop.
        """
        for i in tracks:
            self.m_active_tracks.discard(i)
        self.m_music.stop_multiple_tracks(tracks)

    def fade_in(self, track: int) -> None:
        """
        Fades in a single music track.

        Args:
            track (int): The index of the track to fade in.
        """
        self.m_music.fade_in(track)

    def fade_in_multiple(self, tracks: list[int]) -> None:
        """
        Fades in multiple music tracks.

        Args:
            tracks (list[int]): The list of track indices to fade in.
        """
        self.m_music.fade_in_multiple(tracks)

    def fade_out(self, track: int) -> None:
        """
        Fades out a single music track.

        Args:
            track (int): The index of the track to fade out.
        """
        self.m_music.fade_out(track)

    def fade_out_multiple(self, tracks: list[int]) -> None:
        """
        Fades out multiple music tracks.

        Args:
            tracks (list[int]): The list of track indices to fade out.
        """
        self.m_music.fade_out_multiple(tracks)

    def silent_start_track(self, track: int) -> None:
        """
        Silently starts a single music track (with volume 0).

        Args:
            track (int): The index of the track to start silently.
        """
        self.m_music.start_track_silent(track)

    def silent_start_tracks(self, tracks: list[int]) -> None:
        """
        Silently starts multiple music tracks (with volume 0).

        Args:
            tracks (list[int]): The list of track indices to start silently.
        """
        self.m_music.start_multiple_tracks_silent(tracks)

    def stop_music(self) -> None:
        """
        Stops all currently playing music tracks.
        """
        self.m_active_tracks.clear()
        self.m_music.stop()

    def switch_music_to(self, music_id: int) -> None:
        """
        Switches to a new set of music tracks, fading out the current tracks and fading in the new tracks.

        Args:
            music_id (int): The ID of the new music tracks to switch to.
        """
        self.m_music.fade_out_all()
        self.m_music.start_multiple_tracks(assets.MUSIC_TRACKS[music_id])

    def switch_music_to_loop(self, music_id: int) -> None:
        """
        Switches to a new set of music tracks, fading out the current tracks and fading in the new tracks without restarting them.

        Args:
            music_id (int): The ID of the new music tracks to switch to.
        """
        self.m_music.fade_out_all()
        self.m_music.fade_in_multiple(assets.MUSIC_TRACKS[music_id])
