from abc import abstractmethod
from pygame import Rect

import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from components.game_object import GameObject


class Entity(GameObject):
    """
    An abstract base class that represents an entity in the game.

    Attributes:
        m_max_hp (int): The maximum health points of the entity.
        m_hp (int): The current health points of the entity.
        m_assets (AssetManager): The asset manager for loading assets.
        m_audio (AudioManager): The audio manager for playing sounds.
        m_stage (Stage): The stage on which the entity exists.
        m_speed (float): The speed of the entity.
        m_acceleration (float): The acceleration of the entity.
        m_x_speed (float): The horizontal speed of the entity.
        m_y_speed (float): The vertical speed of the entity.
        m_last_pos (tuple[int, int]): The last position of the entity.
    """

    def __init__(
        self,
        hp: int,
        speed: float,
        bounds: Rect,
        acceleration: float = 0.05,
        stage=None,
    ):
        """
        Constructor for the Entity class.

        Args:
            hp (int): The health points of the entity.
            speed (float): The speed of the entity.
            bounds (Rect): The rectangular bounds of the entity.
            acceleration (float, optional): The acceleration of the entity. Defaults to 0.05.
            stage (Stage, optional): The stage on which the entity exists. Defaults to None.
        """
        super().__init__(bounds)
        self.m_max_hp: int = hp
        self.m_hp: int = hp

        self.m_assets = AssetManager()
        self.m_audio = AudioManager()
        self.m_stage = stage

        # Movement
        self.m_speed: float = speed
        self.m_acceleration: float = acceleration
        self.m_x_speed: float = 0
        self.m_y_speed: float = 0

        self.m_last_pos: tuple[int, int] = self.m_bounds.center

    @property
    def hp(self) -> int:
        """
        Gets the current health points of the entity.

        Returns:
            int: The current health points.
        """
        return self.m_hp

    @property
    def max_hp(self) -> int:
        """
        Gets the maximum health points of the entity.

        Returns:
            int: The maximum health points.
        """
        return self.m_max_hp

    @property
    def speed(self) -> float:
        """
        Gets the speed of the entity.

        Returns:
            float: The speed of the entity.
        """
        return self.m_speed

    def take_damage(self, dmg: int):
        """
        Reduces the entity's health points by the specified damage amount and plays a hit sound effect.

        Args:
            dmg (int): The damage amount.
        """
        self.m_audio.play_sfx(assets.SFX_HIT)
        self.m_hp -= dmg

    @abstractmethod
    def update(self) -> None:
        """
        Abstract method for updating the entity. Must be implemented by subclasses.
        """
        pass

    def move_value_toward(self, value: float, target: float, step: float):
        """
        Moves a value toward a target value by a specific step.

        Args:
            value (float): The current value.
            target (float): The target value.
            step (float): The step size.

        Returns:
            float: The updated value.
        """
        if value < target:
            return min(target, value + step)
        else:
            return max(target, value - step)

    def move_toward(self, position: tuple[int, int]):
        """
        Moves the entity toward a point in a straight line.

        Args:
            position (tuple[int, int]): The target position.
        """
        direction_speed = self.get_diagonal_ratio(
            self.get_angle_to(position)
        )  # get the target directional speeds

        # smooth out movement by using acceleration for directional speeds
        self.m_x_speed = self.move_value_toward(
            self.m_x_speed, direction_speed[0], self.m_acceleration
        )  # set the directional speeds
        self.m_y_speed = self.move_value_toward(
            self.m_y_speed, direction_speed[1], self.m_acceleration
        )  #   by accelerating / decelerating

        self.bounds.move_ip(
            self.m_x_speed * self.m_speed, self.m_y_speed * self.m_speed
        )  # actually move the entity

    def take_knockback_old(self, knockback: tuple[float, float, float]) -> None:
        """
        Applies knockback to the entity using the old method.

        Args:
            knockback (tuple[float, float, float]): The knockback values.
        """
        self.m_bounds.move_ip(knockback[0] * knockback[2], knockback[1] * knockback[2])
        self.m_x_speed = knockback[0]
        self.m_y_speed = knockback[1]

    def take_knockback(self, other, knockback: int = 0) -> None:
        """
        Applies knockback to the entity from another entity.

        Args:
            other (GameObject): The other game object causing the knockback.
            knockback (int, optional): The knockback force. Defaults to 0.
        """
        direction = other.get_diagonal_ratio(other.get_angle_to(self.m_bounds.center))
        self.m_x_speed = direction[0]
        self.m_y_speed = direction[1]
        self.m_bounds.move_ip(direction[0] * knockback, direction[1] * knockback)

    def set_stage(self, stage) -> None:
        """
        Sets the stage for the entity.

        Args:
            stage (Stage): The stage to set.
        """
        self.m_stage = stage

    def collides_with(self, other: GameObject) -> bool:
        """
        Checks if the entity collides with another game object.

        Args:
            other (GameObject): The other game object.

        Returns:
            bool: True if collides, False otherwise.
        """
        return self.m_bounds.colliderect(other.bounds)

    def handle_collisions(self) -> None:
        """
        Handles collisions with other objects. To be implemented by subclasses.
        """
        pass

    def collide(self, other: GameObject) -> None:
        """
        Defines behavior when the entity collides with another game object.

        Args:
            other (GameObject): The other game object.
        """
        pass

    def get_direction(self) -> tuple[float, float]:
        """
        Gets the current direction of the entity.

        Returns:
            tuple[float, float]: The current direction.
        """
        return (self.m_x_speed, self.m_y_speed)

    def handle_wall_collision(self, wall) -> None:
        """
        Handles collision with a wall.

        Args:
            wall (Wall): The wall object.
        """
        # Calculate overlap on each axis
        overlap_x = min(
            self.m_bounds.right - wall.bounds.left, wall.bounds.right - self.m_bounds.left
        )
        overlap_y = min(
            self.m_bounds.bottom - wall.bounds.top, wall.bounds.bottom - self.m_bounds.top
        )

        # Resolve the smaller overlap first (prevents sticking issues)
        if overlap_x < overlap_y:
            if self.m_bounds.centerx < wall.bounds.centerx:
                self.m_bounds.right = wall.bounds.left  # Push left
            else:
                self.m_bounds.left = wall.bounds.right  # Push right
            self.m_x_speed = 0
        else:
            if self.m_bounds.centery < wall.bounds.centery:
                self.m_bounds.bottom = wall.bounds.top  # Push up
            else:
                self.m_bounds.top = wall.bounds.bottom  # Push down
            self.m_y_speed = 0
