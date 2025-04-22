import pygame
from components.game_object import GameObject
from components.entities.entity import Entity


class Stone(Entity):
    """
    Represents a stone projectile in the game.

    Attributes:
        m_x_speed (float): The x-component of the stone's movement direction.
        m_y_speed (float): The y-component of the stone's movement direction.
        m_radius (int): The radius of the stone.
        m_damage (int): The damage dealt by the stone.
        m_color (tuple[int, int, int]): The color of the stone.
    """

    @property
    def damage(self) -> int:
        """
        Gets the damage dealt by the stone.

        Returns:
            int: The damage dealt by the stone.
        """
        return self.m_damage

    def __init__(
        self,
        speed: float,
        start_pos: tuple[int, int],
        diagonals: tuple[float, float],
        radius: int,
        damage: int,
        flight_duration: int,
        stage,
        color: tuple[int, int, int] = (120, 120, 120),
    ):
        """
        Initializes a Stone object.

        Args:
            speed (float): The speed of the stone.
            start_pos (tuple[int, int]): The starting position of the stone.
            diagonals (tuple[float, float]): The directional speeds (should add up to about 1).
            radius (int): The radius of the stone.
            damage (int): The damage dealt by the stone.
            flight_duration (int): The lifespan of the stone in frames.
            stage: The stage in which the stone exists.
            color (tuple[int, int, int], optional): The color of the stone. Defaults to (120, 120, 120).
        """
        super().__init__(
            flight_duration,
            speed,
            pygame.Rect(start_pos[0], start_pos[1], radius * 2, radius * 2),
            stage=stage,
        )
        self.m_x_speed = diagonals[0]
        self.m_y_speed = diagonals[1]
        self.m_radius = radius
        self.m_damage = damage
        self.m_color = color

    def update(self) -> None:
        """
        Updates the state of the stone, including movement and collision handling.
        """
        self.handle_collisions()
        self.m_bounds.move_ip(self.m_x_speed * self.m_speed, self.m_y_speed * self.m_speed)
        self.m_hp -= 1
        if self.m_hp <= 0:
            self.delete()

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the stone on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        pygame.draw.circle(window, self.m_color, self.m_bounds.center, self.m_radius)
        pygame.draw.circle(window, (0, 0, 0), self.m_bounds.center, self.m_radius, width=2)

    def handle_collisions(self) -> None:
        """
        Handles collisions with nearby objects.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            if self.m_stage.get_object_type(o) == self.m_stage.WALL:
                if self.collides_with(o):
                    self.delete()

    def collide(self, other: GameObject, type_id: int = -1) -> None:
        """
        Handles collision with another game object.

        Args:
            other (GameObject): The other game object.
            type_id (int, optional): The type ID of the other game object. Defaults to -1.
        """
        if type_id == self.m_stage.PLAYER:
            self.delete()
