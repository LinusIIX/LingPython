import pygame, math
from components.entities.entity import Entity
from components.entities.projectiles.explosion import Explosion
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class Grenade(Entity):
    """
    Represents a grenade projectile in the game that moves towards a target position and explodes upon reaching it.
    """

    def __init__(
        self,
        speed: float,
        damage: int,
        explosion_radius: int,
        bounds: pygame.Rect,
        target_position: tuple[int, int],
        stage,
    ):
        """
        Initializes a Grenade object.

        Args:
            speed (float): The speed of the grenade.
            damage (int): The damage dealt by the grenade explosion.
            explosion_radius (int): The radius of the explosion.
            bounds (pygame.Rect): The rectangular bounds of the grenade.
            target_position (tuple[int, int]): The target position the grenade moves towards.
            stage: The stage in which the grenade exists.
        """
        super().__init__(1, speed, bounds, acceleration=1, stage=stage)

        self.m_target_pos = target_position
        self.m_total_distance = self.distance_to(self.m_target_pos)
        self.m_remaining_distance = self.m_total_distance

        self.m_damage = damage
        self.m_base_size: int = self.m_bounds.width
        self.m_size: float = 1.0

        asset_manager = AssetManager()
        self.m_spritesheet = SpriteSheet(
            asset_manager.get_image(assets.SPRITESHEET_WEAPONS), 32, 32
        )

    def update(self) -> None:
        """
        Updates the state of the grenade, including movement and size change.
        """
        self.move_toward(self.m_target_pos)

        self.m_remaining_distance = self.distance_to(self.m_target_pos)
        if self.m_remaining_distance < self.m_speed:
            self.m_hp = 0
            return
        progress = self.m_remaining_distance / self.m_total_distance
        self.m_size = 1 + 2 * math.sin(progress * math.pi)

        current_center = self.m_bounds.center
        self.m_bounds.width = self.m_base_size * self.m_size
        self.m_bounds.height = self.m_base_size * self.m_size
        self.m_bounds.center = current_center

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the grenade on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        window.blit(
            self.m_spritesheet.get_sprite_sized(
                assets.WEAPON_GRENADE, self.m_bounds.width, self.m_bounds.height
            ),
            (self.m_bounds.x, self.m_bounds.y),
        )

    def delete(self) -> None:
        """
        Deletes the grenade and spawns an explosion at the current position.
        """
        super().delete()
        self.m_stage.spawn_game_object(
            Explosion(self.m_bounds.center, 128, 25, 35, 30, self.m_stage)
        )
        # TODO: spawn explosion with center at current center
