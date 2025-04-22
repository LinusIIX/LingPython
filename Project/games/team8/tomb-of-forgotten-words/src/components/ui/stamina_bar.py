import pygame


class StaminaBar:
    """
    Represents a stamina bar for a player in the game.

    Attributes:
        m_bounds (pygame.Rect): The bounding rectangle of the stamina bar.
        m_player: The player object to which the stamina bar is attached.
        m_inner (pygame.Rect): The inner rectangle representing the current stamina.
        m_y_offset (int): The vertical offset of the stamina bar relative to the player.
        m_bg_color (tuple[int, int, int]): The background color of the stamina bar.
        m_fill_color (tuple[int, int, int]): The fill color of the stamina bar.
    """

    def __init__(self, bounds: pygame.Rect, player, y_offset: int):
        """
        Initializes a StaminaBar object.

        Args:
            bounds (pygame.Rect): The bounding rectangle of the stamina bar.
            player: The player object to which the stamina bar is attached.
            y_offset (int): The vertical offset of the stamina bar relative to the player.
        """
        self.m_bounds = bounds
        self.m_player = player
        self.m_inner = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.m_y_offset = y_offset
        self.m_bg_color = (0, 0, 0)
        self.m_fill_color = (235, 201, 52)

    def update(self) -> None:
        """
        Updates the position and size of the stamina bar based on the player's stamina.
        """
        if self.m_player.stamina == self.m_player.max_stamina:
            return

        # position bars
        self.m_bounds.center = self.m_player.center
        self.m_bounds.move_ip(0, self.m_y_offset)
        self.m_inner.topleft = self.m_bounds.topleft

        # get stamina in percentage (0 - 1 float)
        stamina = self.m_player.stamina / self.m_player.max_stamina

        # set width of inner bar
        width = self.m_bounds.width * stamina
        self.m_inner.width = max(width, 0)

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the stamina bar on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if self.m_player.stamina == self.m_player.max_stamina:
            return
        pygame.draw.rect(window, self.m_bg_color, self.m_bounds)
        pygame.draw.rect(window, self.m_fill_color, self.m_inner)
