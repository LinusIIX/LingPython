import pygame
from components.game_object import GameObject
from utils.assets.asset_manager import AssetManager


class Wall(GameObject):
    """
    Represents a wall in the game that can be rendered with a sprite.

    Attributes:
        m_sprite_sname (str): The name of the sprite.
        m_sprite (pygame.Surface): The sprite image for the wall.
        m_sprite_size (int): The size of the sprite (assumed to be a square).
        m_rows (int): The number of rows of sprites to fill the wall bounds.
        m_cols (int): The number of columns of sprites to fill the wall bounds.
    """

    def __init__(self, bounds: pygame.Rect, sprite_name: str = None, sprite_size: int = 32):
        """
        Initializes a Wall object.

        Args:
            bounds (pygame.Rect): The rectangular bounds of the wall.
            sprite_name (str, optional): The name of the sprite to render. Defaults to None.
            sprite_size (int, optional): The size of the sprite (assumed to be a square). Defaults to 32.
        """
        super().__init__(bounds)
        self.m_sprite_sname = sprite_name
        self.m_sprite = None
        self.m_sprite_size = sprite_size  # assume that the sprite is a square
        asset_manager = AssetManager()
        if sprite_name:
            self.m_sprite = asset_manager.get_image_scaled(
                sprite_name, (self.m_sprite_size, self.m_sprite_size)
            )

        self.m_rows = self.m_bounds.height // self.m_sprite_size
        self.m_cols = self.m_bounds.width // self.m_sprite_size

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the wall on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if self.m_sprite:
            for i in range(self.m_rows):
                for j in range(self.m_cols):
                    xpos = self.m_bounds.left + j * self.m_sprite_size
                    ypos = self.m_bounds.top + i * self.m_sprite_size
                    window.blit(self.m_sprite, (xpos, ypos))
