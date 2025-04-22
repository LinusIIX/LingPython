import pygame


class MusicPlayer:
    """
    Manages the playback and volume control of multiple music tracks.

    Attributes:
        m_volume (float): The master volume level.
        m_tracks (list[pygame.mixer.Sound]): The list of music tracks.
        m_fade_speed (float): The speed at which tracks fade in and out.
        m_channels (list[pygame.mixer.Channel]): The list of mixer channels for the tracks.
        m_track_states (dict[int, dict]): The state of each track including volume and fading status.
    """

    def __init__(
        self, tracks: list[pygame.mixer.Sound], fade_speed: float = 1, start_volume: float = 1
    ):
        """
        Initializes a MusicPlayer object.

        Args:
            tracks (list[pygame.mixer.Sound]): The list of music tracks.
            fade_speed (float, optional): The speed at which tracks fade in and out. Defaults to 1.
            start_volume (float, optional): The initial master volume level. Defaults to 1.
        """
        self.m_volume = start_volume
        self.m_tracks = tracks
        self.m_fade_speed = fade_speed
        self.m_channels = [pygame.mixer.Channel(i) for i in range(len(tracks))]
        self.m_track_states = {
            i: {"volume": 0.0, "target_volume": 0.0, "fading": False} for i in range(len(tracks))
        }

    def play_all(self) -> None:
        """
        Plays all tracks in a loop with initial volume set to 0.
        """
        for i, sound in enumerate(self.m_tracks):
            self.m_channels[i].play(sound, loops=-1)
            self.m_channels[i].set_volume(0.0)

    def fade_in(self, track_index: int, target_volume=None) -> None:
        """
        Fades in a specific track to the target volume.

        Args:
            track_index (int): The index of the track to fade in.
            target_volume (float, optional): The target volume level. Defaults to 1.0.
        """
        if target_volume is None:
            target_volume = 1.0

        if not self.m_channels[
            track_index
        ].get_busy():  # check if the track isn't playing, if so, start it
            self.start_track(track_index)

        self.m_track_states[track_index]["target_volume"] = target_volume
        self.m_track_states[track_index]["fading"] = True

    def fade_out(self, track_index: int) -> None:
        """
        Fades out a specific track.

        Args:
            track_index (int): The index of the track to fade out.
        """
        self.m_track_states[track_index]["target_volume"] = 0.0
        self.m_track_states[track_index]["fading"] = True

    def update(self) -> None:
        """
        Updates the volume of all tracks based on their fading status.
        """
        for i, channel in enumerate(self.m_channels):
            state = self.m_track_states[i]
            current_vol = state["volume"]
            target_volume = state["target_volume"]
            if state["fading"]:
                if current_vol < target_volume:
                    current_vol = min(current_vol + self.m_fade_speed, target_volume)
                elif current_vol > target_volume:
                    current_vol = max(current_vol - self.m_fade_speed, target_volume)

                self.m_track_states[i]["volume"] = current_vol
                channel.set_volume(current_vol * self.m_volume)

                if current_vol == target_volume:
                    self.m_track_states[i]["fading"] = False

    def fade_in_multiple(self, tracks: list[int]) -> None:
        """
        Fades in multiple tracks.

        Args:
            tracks (list[int]): The list of track indices to fade in.
        """
        for i in tracks:
            self.fade_in(i)

    def fade_out_multiple(self, tracks: list[int]) -> None:
        """
        Fades out multiple tracks.

        Args:
            tracks (list[int]): The list of track indices to fade out.
        """
        for i in tracks:
            self.fade_out(i)

    def fade_out_all(self) -> None:
        """
        Fades out all tracks.
        """
        for i in range(len(self.m_tracks)):
            self.fade_out(i)

    def stop(self) -> None:
        """
        Stops all tracks.
        """
        for channel in self.m_channels:
            channel.stop()

    def stop_track(self, track: int) -> None:
        """
        Stops a specific track.

        Args:
            track (int): The index of the track to stop.
        """
        self.m_channels[track].stop()

    def start_track(self, track: int) -> None:
        """
        Starts playing a specific track and fades it in.

        Args:
            track (int): The index of the track to start.
        """
        self.start_track_silent(track)
        self.fade_in(track)

    def start_track_silent(self, track: int) -> None:
        """
        Starts playing a specific track with volume set to 0.

        Args:
            track (int): The index of the track to start.
        """
        if self.m_channels[track].get_busy():  # restart the track if it's already running
            self.m_channels[track].stop()
        self.m_channels[track].play(self.m_tracks[track], loops=-1)
        self.m_channels[track].set_volume(0)

    def stop_multiple_tracks(self, tracks: list[int]) -> None:
        """
        Stops multiple tracks.

        Args:
            tracks (list[int]): The list of track indices to stop.
        """
        for i in tracks:
            self.stop_track(i)

    def start_multiple_tracks(self, tracks: list[int]) -> None:
        """
        Starts playing multiple tracks and fades them in.

        Args:
            tracks (list[int]): The list of track indices to start.
        """
        for i in tracks:
            self.start_track(i)

    def start_multiple_tracks_silent(self, tracks: list[int]) -> None:
        """
        Starts playing multiple tracks with volume set to 0.

        Args:
            tracks (list[int]): The list of track indices to start.
        """
        for i in tracks:
            self.start_track_silent(i)

    def quit(self) -> None:
        """
        Quits the mixer.
        """
        pygame.mixer.quit()

    def set_master_volume(self, volume: float) -> None:
        """
        Sets the master volume level.

        Args:
            volume (float): The new master volume level (0.0 to 1.0).
        """
        if 0 <= volume <= 1:
            self.m_volume = volume
            for i, channel in enumerate(self.m_channels):
                channel.set_volume(self.m_track_states[i]["volume"] * self.m_volume)
