import pygame
import utils.assets.asset_keys as assets
from components.game_object import GameObject
from utils.assets.asset_manager import AssetManager


class Cobweb(GameObject):
    """
    Represents a cobweb obstacle in the game that slows down entities and fades out over time.

    Attributes:
        m_fadeout_time (int): The time in frames for the cobweb to fade out without being an obstacle.
        m_start_lifespan (int): The initial lifespan of the cobweb including fadeout time.
        m_lifespan (int): The current lifespan of the cobweb including fadeout time.
        m_sprite (pygame.Surface): The sprite image for the cobweb.
        m_alpha (int): The alpha transparency value of the cobweb sprite.
        m_active (bool): Indicates if the cobweb is active and can slow down entities.
    """

    @property
    def active(self) -> bool:
        """
        Gets the active status of the cobweb.

        Returns:
            bool: True if the cobweb is active, False otherwise.
        """
        return self.m_active

    @property
    def alpha(self) -> int:
        """
        Gets the alpha transparency value of the cobweb sprite.

        Returns:
            int: The alpha transparency value.
        """
        return self.m_alpha

    def __init__(self, bounds: pygame.Rect, lifespan: int):
        """
        Initializes a Cobweb object.

        Args:
            bounds (pygame.Rect): The rectangular bounds of the cobweb.
            lifespan (int): The lifespan of the cobweb in frames.
        """
        super().__init__(bounds)
        asset_manager = AssetManager()
        self.m_fadeout_time: int = (
            30  # for 30 frames the cobweb fades out without actually being an obstacle
        )
        self.m_start_lifespan: int = lifespan + self.m_fadeout_time
        self.m_lifespan: int = lifespan + self.m_fadeout_time
        self.m_sprite: pygame.Surface = asset_manager.get_image_scaled(
            assets.SPRITE_COBWEB, (self.m_bounds.width, self.m_bounds.height)
        )
        self.m_alpha: int = 255
        self.m_active: bool = True


    def update(self) -> None:
        """
        Updates the cobwebs lifespan and state.
        """
        self.m_lifespan -= 1
        self.m_to_be_deleted = self.m_lifespan <= 0
        

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the cobweb on the given window surface

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if (
            self.m_lifespan < 180
        ):  # only start to fade out if the time the web exists is less than 3 seconds (180 frames)
            self.m_active = self.m_active > self.m_fadeout_time
            self.m_alpha = max(
                0, int(255 * (self.m_lifespan / self.m_start_lifespan))
            )  # fade out with lifespan running out

        self.m_sprite.set_alpha(self.m_alpha)
        window.blit(self.m_sprite, self.m_bounds.topleft)
