import pygame
from components.entities.entity import Entity


class HealthBar:
    """
    Represents a health bar for an entity in the game.
    """

    def __init__(self, entity: Entity, bounds: pygame.Rect, y_offset: int):
        """
        Initializes a HealthBar object.

        Args:
            entity (Entity): The entity to which the health bar is attached.
            bounds (pygame.Rect): The bounding rectangle of the health bar.
            y_offset (int): The vertical offset of the health bar relative to the entity.
        """
        self.m_entity: Entity = entity
        self.m_bounds: pygame.Rect = bounds
        self.m_inner: pygame.Rect = pygame.Rect(0, 0, bounds.width - 4, bounds.height - 4)
        self.m_y_offset: int = y_offset
        self.bg_color: tuple[int, int, int] = (30, 30, 30, 80)
        self.m_color: tuple[int, int, int] = (0, 255, 0, 100)

    def update(self) -> None:
        """
        Updates the position and size of the health bar based on the entity's health.
        """
        # Update position relative to entity
        self.m_bounds.center = self.m_entity.bounds.center
        self.m_bounds.move_ip(0, self.m_y_offset)
        self.m_inner.topleft = self.m_bounds.topleft
        self.m_inner.move_ip(2, 2)

        # Calculate relative HP
        health = self.m_entity.hp / self.m_entity.max_hp

        # Set width of inner bar
        width = (self.m_bounds.width - 4) * health
        self.m_inner.width = max(width, 0)

        # Update color of inner fill box
        health_col = max(0, int(255 * health))
        self.m_color = (255 - health_col, health_col, 0, 100)

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the health bar on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        pygame.draw.rect(window, self.bg_color, self.m_bounds)
        pygame.draw.rect(window, self.m_color, self.m_inner)
