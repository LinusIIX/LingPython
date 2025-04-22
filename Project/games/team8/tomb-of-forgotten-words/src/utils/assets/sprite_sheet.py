from pygame import Surface, Rect, transform


class SpriteSheet:
    """
    Represents a sprite sheet and provides methods to extract and manipulate individual sprites.
    """

    def __init__(self, image: Surface, cell_width: int, cell_height: int):
        """
        Initializes a SpriteSheet object.

        Args:
            image (Surface): The sprite sheet image.
            cell_width (int): The width of each cell in the sprite sheet.
            cell_height (int): The height of each cell in the sprite sheet.
        """
        self.m_sheet = image
        self.m_cell_width = cell_width
        self.m_cell_height = cell_height
        self.m_cols = self.m_sheet.get_width() / self.m_cell_width

    def get_sprite(self, pos: int) -> Surface:
        """
        Returns a sprite in the sprite sheet at the specified position.

        Args:
            pos (int): The position of the sprite in the sprite sheet (row * cols + col).

        Returns:
            Surface: The extracted sprite.

        Raises:
            ValueError: If the position is out of bounds.
        """
        x: int = (
            pos % self.m_cols
        ) * self.m_cell_width  # modulo to get which column the sprite is in
        y: int = (
            pos // self.m_cols
        ) * self.m_cell_height  # integer division to get which row the sprite is in

        if (x + self.m_cell_width > self.m_sheet.get_width()) or (
            y + self.m_cell_height > self.m_sheet.get_height()
        ):
            x = 0  # if the position is out of bounds return the first sprite
            y = 0  # in order to avoid crashes
            print(f"Error: position '{pos}' is out of bounds!")
        return self.m_sheet.subsurface(Rect(x, y, self.m_cell_width, self.m_cell_height))

    def get_sprite_sized(self, pos: int, width: int, height: int) -> Surface:
        """
        Returns a sprite in the sprite sheet at the specified position, scaled to the given width and height.

        Args:
            pos (int): The position of the sprite in the sprite sheet (row * cols + col).
            width (int): The desired width of the sprite.
            height (int): The desired height of the sprite.

        Returns:
            Surface: The extracted and scaled sprite.
        """
        return transform.scale(self.get_sprite(pos), (width, height))
