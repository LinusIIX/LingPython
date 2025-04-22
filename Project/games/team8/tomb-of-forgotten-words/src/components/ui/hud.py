import pygame
from components.ui.inventory import Inventory
from components.ui.recharge_inventory import RechargeInventory
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class HUD:
    """
    Singleton class that manages all the heads-up display (HUD) UI components.
    Allows all components to access it without needing to pass it from the game class.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.m_initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the HUD object.
        """
        if self.m_initialized:
            return
        self.m_initialized = True

        self.m_inventory_tile_size = 60
        self.m_assets = AssetManager()
        weapons_spritesheet = SpriteSheet(
            self.m_assets.get_image(assets.SPRITESHEET_WEAPONS), 32, 32
        )
        weapons_inventory = [
            weapons_spritesheet.get_sprite_sized(
                assets.WEAPON_REVOLVER, self.m_inventory_tile_size, self.m_inventory_tile_size
            ),
            weapons_spritesheet.get_sprite_sized(
                assets.WEAPON_SHOTGUN, self.m_inventory_tile_size, self.m_inventory_tile_size
            ),
            weapons_spritesheet.get_sprite_sized(
                assets.WEAPON_MACHINE_GUN, self.m_inventory_tile_size, self.m_inventory_tile_size
            ),
        ]
        self.m_inventory = Inventory(32, 32, self.m_inventory_tile_size, weapons_inventory, gap=4)

        self.m_grenade_slot = RechargeInventory(
            1280 - 92,
            32,
            self.m_inventory_tile_size,
            weapons_spritesheet.get_sprite_sized(
                assets.WEAPON_GRENADE, self.m_inventory_tile_size, self.m_inventory_tile_size
            ),
            ignore_top=14,
            ignore_bottom=9,
        )

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the HUD components on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        self.m_inventory.render(window)
        self.m_grenade_slot.render(window)

    def update_inventory_selection(self, selection: int) -> None:
        """
        Updates the inventory selection.

        Args:
            selection (int): The index of the selected inventory item.
        """
        self.m_inventory.set_selected(selection)

    def update_grenade_recharge(self, progress: float) -> None:
        """
        Updates the grenade recharge progress.

        Args:
            progress (float): The progress of the grenade recharge (0.0 to 1.0).
        """
        self.m_grenade_slot.update_progress(progress)
