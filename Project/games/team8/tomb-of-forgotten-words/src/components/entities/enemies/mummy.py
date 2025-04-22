import pygame
import random
from components.entities.enemies.enemy import Enemy
from components.entities.animated_entity import AnimatedEntity
from components.entities.projectiles.bullet import Bullet
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class Mummy(Enemy, AnimatedEntity):
    """
    Represents a Mummy enemy entity with animation capabilities.

    Attributes:
        m_spritesheet (SpriteSheet): The spritesheet used for mummy animations.
        m_wobble_intensity (float): The intensity of the mummy's wobble movement.
    """

    def __init__(
        self,
        hp: int,
        speed: float,
        bounds: pygame.Rect,
        stage,
        knockback: int,
        acceleration: float = 0.5,
        damage: int = 0,
    ):
        """
        Initializes a Mummy object.

        Args:
            hp (int): The health points of the mummy.
            speed (float): The speed of the mummy.
            bounds (pygame.Rect): The rectangular bounds of the mummy.
            stage (Stage): The stage on which the mummy exists.
            knockback (int): The knockback force of the mummy.
            acceleration (float, optional): The acceleration of the mummy. Defaults to 0.5.
            damage (int, optional): The damage dealt by the mummy. Defaults to 0.
        """
        Enemy.__init__(
            self, hp, speed, bounds, damage, knockback, pygame.Rect(0, 0, 100, 15), -100, stage
        )
        AnimatedEntity.__init__(self, 15, assets.MUMMY)

        asset_manager = AssetManager()
        self.m_spritesheet = SpriteSheet(asset_manager.get_image(assets.SPRITESHEET_MUMMY), 32, 32)

        self.m_wobble_intensity = 3

    def update(self) -> None:
        """
        Updates the state of the mummy, including movement and collision handling.
        """
        self.move_toward(self.m_stage.player_center)
        self.handle_collisions()

        self.m_health_bar.update()

    def handle_collisions(self) -> None:
        """
        Handles collisions with nearby objects.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            obj_type = self.m_stage.get_object_type(o)
            match (obj_type):
                case self.m_stage.WALL:
                    if self.collides_with(o):
                        self.handle_wall_collision(o)

    def move_toward(self, position: tuple[int, int]) -> None:
        """
        Moves the mummy toward a target position with a wobble effect to avoid bullets.

        Args:
            position (tuple[int, int]): The target position.
        """
        direction_speed = self.get_diagonal_ratio(self.get_angle_to(position))

        wobble_x = random.uniform(-self.m_wobble_intensity, self.m_wobble_intensity)
        wobble_y = random.uniform(-self.m_wobble_intensity, self.m_wobble_intensity)

        self.m_x_speed = self.move_value_toward(
            self.m_x_speed, direction_speed[0] + wobble_x, self.m_acceleration
        )
        self.m_y_speed = self.move_value_toward(
            self.m_y_speed, direction_speed[1] + wobble_y, self.m_acceleration
        )

        self.bounds.move_ip(self.m_x_speed * self.m_speed, self.m_y_speed * self.m_speed)

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the mummy on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        window.blit(
            self.m_spritesheet.get_sprite_sized(
                self.m_sprite, self.m_bounds.width, self.m_bounds.height
            ),
            (self.m_bounds.x, self.m_bounds.y),
        )
        self.m_health_bar.render(window)
