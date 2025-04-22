import pygame
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from components.entities.entity import Entity
from components.ui.health_bar import HealthBar


class Enemy(Entity):
    """
    Represents an enemy entity in the game.
    """

    @property
    def knockback(self) -> int:
        """
        Gets the knockback force of the enemy.

        Returns:
            int: The knockback force.
        """
        return self.m_knockback

    @property
    def damage(self) -> int:
        """
        Gets the damage dealt by the enemy.

        Returns:
            int: The damage.
        """
        return self.m_damage

    def __init__(
        self,
        hp: int,
        speed: float,
        bounds: pygame.Rect,
        damage: int,
        knockback: int,
        hp_bar_bounds: pygame.Rect,
        hp_bar_offset: int,
        stage,
    ):
        """
        Initializes an Enemy object.

        Args:
            hp (int): The health points of the enemy.
            speed (float): The speed of the enemy.
            bounds (pygame.Rect): The rectangular bounds of the enemy.
            damage (int): The damage dealt by the enemy.
            knockback (int): The knockback force of the enemy.
            hp_bar_bounds (pygame.Rect): The bounds of the health bar.
            hp_bar_offset (int): The offset of the health bar.
            stage (Stage): The stage on which the enemy exists.
        """
        super().__init__(hp, speed, bounds, stage=stage)

        self.m_damage = damage
        self.m_knockback = knockback

        self.m_health_bar = HealthBar(self, hp_bar_bounds, hp_bar_offset)

    def hit_entity(self, other: Entity) -> tuple[float, float, float]:
        """
        Checks if the enemy hits another entity.

        If the entities are colliding, it returns a tuple with the knockback speeds for each direction
        depending on the angle of the collision. If the two entities are not colliding, None is returned.

        Args:
            other (Entity): The entity to check for collision.

        Returns:
            tuple[float, float, float]: The knockback speeds for each direction if colliding, otherwise None.
        """
        if self.m_bounds.colliderect(other.bounds):
            return (self.m_x_speed, self.m_y_speed, self.m_knockback)
        return None

    def take_knockback(self, other: Entity, knockback: int = 0) -> None:
        """
        Applies knockback to the enemy from another entity and updates the health_bar position.

        Args:
            other (GameObject): The other game object causing the knockback.
            knockback (int, optional): The knockback force. Defaults to 0.
        """
        super().take_knockback(other, knockback=knockback)
        self.m_health_bar.update()
