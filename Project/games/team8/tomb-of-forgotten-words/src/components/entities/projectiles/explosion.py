import pygame
from components.game_object import GameObject
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager


class Explosion(GameObject):
    """
    Represents an explosion in the game, dealing damage to nearby objects and rendering an explosion sprite.
    """

    def __init__(
        self,
        position: tuple[int, int],
        radius: int,
        damage: int,
        core_damage: int,
        lifespan: int,
        stage,
    ):
        """
        Initializes an Explosion object.

        Args:
            position (tuple[int, int]): The position of the explosion.
            radius (int): The radius of the explosion.
            damage (int): The base damage dealt by the explosion.
            core_damage (int): The additional damage dealt at the core of the explosion.
            lifespan (int): The lifespan of the explosion in frames.
            stage: The stage in which the explosion exists.
        """
        super().__init__(pygame.Rect(position[0], position[1], radius, radius))
        self.m_bounds.center = position
        self.m_radius = radius
        self.m_position = position
        self.m_lifespan = lifespan
        self.m_start_lifespan = self.m_lifespan

        asset_manager = AssetManager()
        self.m_sprite = asset_manager.get_image_scaled(
            assets.SPRITE_EXPLOSION, (self.m_radius, self.m_radius)
        )
        audio_manager = AudioManager()
        audio_manager.play_sfx(assets.SFX_EXPLOSION)

        self.m_damage = damage
        self.m_core_dmg_bonus = core_damage - self.m_damage

        self.m_stage = stage

        self.m_alpha: int = 255
        self.deal_damage()

    def deal_damage(self) -> None:
        """
        Deals damage to nearby objects within the explosion radius.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            obj_type = self.m_stage.get_object_type(o)
            match (obj_type):
                case self.m_stage.PLAYER | self.m_stage.ENEMY:
                    distance = self.distance_to(o.center)
                    diagonals = self.get_diagonal_ratio(self.get_angle_to(o.center))
                    dmg = self.m_damage + int(
                        self.m_core_dmg_bonus * (1 - (distance / self.m_radius))
                    )
                    o.take_damage(dmg)
                    o.take_knockback(self, knockback=dmg * 2)

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the explosion on the given window surface and updates its lifespan.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        self.m_lifespan -= 1
        self.m_to_be_deleted = self.m_lifespan <= 0

        self.m_alpha = max(0, int(255 * (self.m_lifespan / self.m_start_lifespan)))

        self.m_sprite.set_alpha(self.m_alpha)
        window.blit(self.m_sprite, self.m_bounds.topleft)
