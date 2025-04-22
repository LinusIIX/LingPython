import pygame
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class Inventory:
    """
    Represents an inventory UI component in the game.
    """

    def __init__(
        self,
        x: int,
        y: int,
        tile_size: int,
        inventory: list[pygame.Surface],
        selected: int = 0,
        gap=0,
    ):
        """
        Initializes an Inventory object.

        Args:
            x (int): The x-coordinate of the inventory's position.
            y (int): The y-coordinate of the inventory's position.
            tile_size (int): The size of each inventory tile.
            inventory (list[pygame.Surface]): The list of inventory item sprites.
            selected (int, optional): The index of the currently selected inventory item. Defaults to 0.
            gap (int, optional): The gap between inventory tiles. Defaults to 0.
        """
        self.m_inventory_sprites = inventory
        self.m_x = x
        self.m_y = y
        self.m_tile_size = tile_size
        asset_manager = AssetManager()
        self.m_spritesheet = SpriteSheet(
            asset_manager.get_image(assets.SPRITESHEET_INVENTORY_SLOT), 32, 32
        )

        self.m_selected = selected
        self.m_gap = gap

    def set_selected(self, selected: int) -> None:
        """
        Sets the selected inventory item.

        Args:
            selected (int): The index of the selected inventory item.
        """
        self.m_selected = max(0, min(selected, len(self.m_inventory_sprites) - 1))

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the inventory on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        x = self.m_x
        y = self.m_y
        for i in range(len(self.m_inventory_sprites)):
            if self.m_selected == i:
                window.blit(
                    self.m_spritesheet.get_sprite_sized(
                        assets.INVENTORY_SELECTED, self.m_tile_size, self.m_tile_size
                    ),
                    (x, y),
                )
            else:
                window.blit(
                    self.m_spritesheet.get_sprite_sized(
                        assets.INVENTORY_UNSELECTED, self.m_tile_size, self.m_tile_size
                    ),
                    (x, y),
                )
            window.blit(self.m_inventory_sprites[i], (x, y))
            x += self.m_tile_size + self.m_gap
