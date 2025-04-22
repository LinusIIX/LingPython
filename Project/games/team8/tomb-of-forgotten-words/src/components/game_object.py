from abc import ABC, abstractmethod
from pygame import Rect, Surface
import math


class GameObject(ABC):
    """Abstract base class for all game objects."""

    @property
    def bounds(self) -> Rect:
        """Gets the bounding rectangle of the object.

        Returns:
            Rect: The bounding rectangle of the object.
        """
        return self.m_bounds

    @property
    def center(self) -> tuple[int, int]:
        """Gets the center position of the object.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the center.
        """
        return self.m_bounds.center

    @property
    def x(self) -> int:
        """Gets the x-coordinate of the object's position.

        Returns:
            int: The x-coordinate of the object.
        """
        return self.m_bounds.x

    @property
    def y(self) -> int:
        """Gets the y-coordinate of the object's position.

        Returns:
            int: The y-coordinate of the object.
        """
        return self.m_bounds.y

    @property
    def width(self) -> int:
        """Gets the width of the object.

        Returns:
            int: The width of the object.
        """
        return self.m_bounds.width

    @property
    def height(self) -> int:
        """Gets the height of the object.

        Returns:
            int: The height of the object.
        """
        return self.m_bounds.height

    @property
    def to_be_deleted(self) -> bool:
        """Checks if the object is marked for deletion.

        Returns:
            bool: True if the object is marked for deletion, False otherwise.
        """
        return self.m_to_be_deleted

    def __init__(self, bounds: Rect):
        """Initializes a GameObject with a bounding rectangle.

        Args:
            bounds (Rect): The bounding rectangle of the object.
        """
        self.m_bounds = bounds
        self.m_to_be_deleted: bool = False

    @abstractmethod
    def render(self, window: Surface) -> None:
        """Abstract method to render the object onto a window.

        Args:
            window (Surface): The Pygame surface to render the object on.
        """
        pass

    def distance_to(self, position: tuple[int, int]) -> float:
        """Calculates the Euclidean distance to a given position.

        Args:
            position (tuple[int, int]): The (x, y) coordinates of the target position.

        Returns:
            float: The distance to the given position.
        """
        a: float = self.m_bounds.centerx - position[0]
        b: float = self.m_bounds.centery - position[1]
        return math.sqrt(a**2 + b**2)

    def get_angle_to(self, position: tuple[int, int]) -> float:
        """Calculates the angle from the object's center to a given position.

        Args:
            position (tuple[int, int]): The (x, y) coordinates of the target position.

        Returns:
            float: The angle in radians.
        """
        dx: float = self.m_bounds.centerx - position[0]
        dy: float = self.m_bounds.centery - position[1]
        return math.atan2(dy, dx)

    def get_diagonal_ratio(self, angle: float) -> tuple[float, float]:
        """Calculates the diagonal movement ratio based on an angle.

        Args:
            angle (float): The angle in radians.

        Returns:
            tuple[float, float]: The (x, y) ratio for diagonal movement.
        """
        return (-math.cos(angle), -math.sin(angle))

    def delete(self) -> None:
        """Marks the object for deletion in the next frame."""
        self.m_to_be_deleted = True
