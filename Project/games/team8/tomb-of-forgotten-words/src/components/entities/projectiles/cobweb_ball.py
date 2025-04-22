from components.entities.entity import Entity
from components.obstacles.cobweb import Cobweb
from components.game_object import GameObject
import pygame


class CobwebBall(Entity):
    """
    CobwebBall is a projectile shot by spiders. If it hits the player, they take damage and a cobweb spawns on them, slowing them down.
    If the ball does not hit the player, it spawns a cobweb after the flight duration runs out.

    Attributes:
        damage (int): The amount of damage the cobweb ball deals.
    """

    @property
    def damage(self) -> int:
        """
        Gets the damage dealt by the cobweb ball.

        Returns:
            int: The damage dealt by the cobweb ball.
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
        web_width: int,
        web_height: int,
        web_lifespan: int,
        stage,
    ):
        """
        Initializes a CobwebBall object.

        Args:
            speed (float): The speed at which the ball flies.
            start_pos (tuple[int, int]): The position at which the ball starts to fly.
            diagonals (tuple[float, float]): The directional speeds (should add up to about 1).
            radius (int): The radius of the ball.
            damage (int): The amount of damage the player will take if hit.
            flight_duration (int): How many frames the ball will fly before landing and creating a cobweb.
            web_width (int): The width of the spawned cobweb.
            web_height (int): The height of the spawned cobweb.
            web_lifespan (int): The lifespan in frames of the spawned cobweb.
            stage: The stage in which the cobweb ball exists.
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
        self.m_cobweb = Cobweb(pygame.Rect(0, 0, web_width, web_height), web_lifespan)
        self.m_damage = damage

    def spawn_cobweb(self) -> None:
        """
        Spawns a cobweb at the current position of the cobweb ball.
        """
        self.m_cobweb.bounds.center = self.m_bounds.center
        self.m_stage.spawn_game_object(self.m_cobweb)

    def update(self) -> None:
        """
        Updates the state of the cobweb ball, including movement and collision handling.
        """
        self.handle_collisions()
        self.m_bounds.move_ip(self.m_x_speed * self.m_speed, self.m_y_speed * self.m_speed)
        self.m_hp -= 1
        if self.m_hp <= 0:
            self.spawn_cobweb()
            self.delete()

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the cobweb ball on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        pygame.draw.circle(window, (250, 254, 248), self.m_bounds.center, self.m_radius)
        pygame.draw.rect(window, (0, 0, 0), self.m_bounds, width=1)

    def collide(self, other: GameObject, type_id: int = -1) -> None:
        """
        Handles collision with another game object.

        Args:
            other (GameObject): The other game object.
            type_id (int, optional): The type ID of the other game object. Defaults to -1.
        """
        if type_id == self.m_stage.PLAYER:
            self.m_bounds.center = other.bounds.center
            self.spawn_cobweb()
            self.m_to_be_deleted = True
            self.m_hp = 0

    def handle_collisions(self) -> None:
        """
        Handles collisions with nearby objects.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            if self.m_stage.get_object_type(o) == self.m_stage.WALL:
                if self.collides_with(o):
                    self.m_to_be_deleted = True
                    self.m_hp = 0
                    self.spawn_cobweb()
