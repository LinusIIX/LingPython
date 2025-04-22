import pygame
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class RechargeInventory:
    """
    Represents a recharge inventory slot with cooldown effect in the game.
    """

    def __init__(
        self,
        x: int,
        y: int,
        tile_size: int,
        sprite: pygame.Surface,
        ignore_top: int = 0,
        ignore_bottom: int = 0,
    ):
        """
        Initializes a RechargeInventory object.

        Args:
            x (int): The x-coordinate of the inventory slot.
            y (int): The y-coordinate of the inventory slot.
            tile_size (int): The size of each inventory tile.
            sprite (pygame.Surface): The sprite image for the inventory item.
            ignore_top (int, optional): The pixel height to ignore from the top of the sprite. Defaults to 0.
            ignore_bottom (int, optional): The pixel height to ignore from the bottom of the sprite. Defaults to 0.
        """
        self.m_x = x
        self.m_y = y
        self.m_tile_size = tile_size

        self.m_transparency: int = 100  # Initial transparency level
        self.m_sprite = sprite

        asset_manager = AssetManager()
        self.m_spritesheet = SpriteSheet(
            asset_manager.get_image(assets.SPRITESHEET_INVENTORY_SLOT), 32, 32
        )

        self.m_progress: float = 1  # Cooldown progress (1 = fully recharged)

        self.m_ignore_top = ignore_top
        self.m_ignore_bottom = ignore_bottom
        self.m_effective_height = self.m_tile_size - (self.m_ignore_top + self.m_ignore_bottom)

    def update_progress(self, progress: float) -> None:
        """
        Updates the cooldown progress.

        Args:
            progress (float): The new cooldown progress value (0.0 to 1.0).
        """
        self.m_progress = max(0, min(progress, 1))  # Clamp between 0 and 1

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the inventory slot and cooldown effect on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if self.m_progress >= 1:
            window.blit(
                self.m_spritesheet.get_sprite_sized(
                    assets.INVENTORY_SELECTED, self.m_tile_size, self.m_tile_size
                ),
                (self.m_x, self.m_y),
            )
            window.blit(self.m_sprite, (self.m_x, self.m_y))
            return

        # Choose the appropriate inventory frame (selected/unselected)
        frame_key = (
            assets.INVENTORY_SELECTED if self.m_progress >= 1.0 else assets.INVENTORY_UNSELECTED
        )
        window.blit(
            self.m_spritesheet.get_sprite_sized(frame_key, self.m_tile_size, self.m_tile_size),
            (self.m_x, self.m_y),
        )

        # Create a semi-transparent faded version of the sprite
        faded_sprite = self.m_sprite.copy()
        faded_sprite.set_alpha(self.m_transparency)
        window.blit(faded_sprite, (self.m_x, self.m_y))

        # Only affect the visible middle part of the sprite
        if self.m_progress > 0:
            visible_height = int(
                self.m_progress * self.m_effective_height
            )  # Only affect the non-transparent part
            y_offset = self.m_ignore_top + (self.m_effective_height - visible_height)

            visible_part = self.m_sprite.subsurface((0, y_offset, self.m_tile_size, visible_height))
            window.blit(visible_part, (self.m_x, self.m_y + y_offset))
