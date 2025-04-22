import pygame
from components.entities.entity import Entity
from components.game_object import GameObject
import utils.assets.asset_keys as assets
from utils.assets.audio_manager import AudioManager


class Bullet(Entity):
    """
    Represents a bullet projectile in the game.

    Attributes:
        m_x (float): The x-component of the bullet's direction.
        m_y (float): The y-component of the bullet's direction.
        m_dmg (int): The damage dealt by the bullet.
        m_center (tuple[int, int]): The center position of the bullet.
    """

    def __init__(
        self,
        speed: float,
        diagonals: tuple[float, float],
        damage: int,
        bounds: pygame.Rect,
        lifespan: int,
    ):
        """
        Initializes a Bullet object.

        Args:
            speed (float): The speed of the bullet.
            diagonals (tuple[float, float]): The x and y components of the bullet's direction.
            damage (int): The damage dealt by the bullet.
            bounds (pygame.Rect): The rectangular bounds of the bullet.
            lifespan (int): The lifespan of the bullet in frames.
        """
        super().__init__(
            lifespan, speed, bounds, None, None
        )  # hp stands for lifespan of bullet, bullet doesn't draw sprites so no asset_manager is needed
        self.m_x = diagonals[0]
        self.m_y = diagonals[1]
        self.m_dmg = damage
        self.m_center = self.m_bounds.center

    def update(self) -> None:
        """
        Updates the state of the bullet, including movement and collision handling.
        """
        self.m_bounds.move_ip(self.m_speed * self.m_x, self.m_speed * self.m_y)
        self.m_center = self.m_bounds.center

        self.handle_collisions()

        self.m_hp -= 1  # tick down hp (lifespan)
        if self.m_hp <= 0:  # if the lifespan of the bullet has ended
            self.delete()

    def handle_collisions(self) -> None:
        """
        Handles collisions of the bullet with other objects.
        """
        if self.m_stage is None:
            return
        hit: bool = False
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            obj_type = self.m_stage.get_object_type(o)
            if obj_type != self.m_stage.PLAYER and obj_type != self.m_stage.BULLET:
                if self.collides_with(o):
                    hit = True
                    if obj_type == self.m_stage.ENEMY:
                        o.take_damage(self.m_dmg)
                        o.take_knockback(self, knockback=self.m_speed * 2)
        if hit:
            self.delete()

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the bullet on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if self.m_bounds.height >= 8:
            pygame.draw.circle(window, (30, 30, 30), self.m_center, self.m_bounds.width / 2)
        pygame.draw.line(
            window,
            (30, 30, 30),
            self.m_center,
            (
                self.m_center[0] - int(self.m_x * self.m_bounds.height),
                self.m_center[1] - int(self.m_y * self.m_bounds.height),
            ),
            width=self.m_bounds.width,
        )
