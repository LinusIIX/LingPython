import pygame
from components.game_object import GameObject


class SpatialGrid:
    """
    A spatial grid for efficiently managing and querying objects in a 2D space.

    Attributes:
        cell_size (int): The size of each cell in the grid.
        m_grid (dict): A dictionary mapping cell coordinates to lists of game objects.
    """

    def __init__(self, cell_size: int):
        """
        Initializes a SpatialGrid object.

        Args:
            cell_size (int): The size of each cell in the grid.
        """
        self.cell_size = cell_size
        self.m_grid = {}

    def get_cell_coords(self, bounds: pygame.Rect) -> list[tuple[int, int]]:
        """
        Gets the coordinates of the cells that intersect with the given bounding rectangle.

        Args:
            bounds (pygame.Rect): The bounding rectangle.

        Returns:
            list[tuple[int, int]]: A list of cell coordinates that intersect with the bounds.
        """
        x1, y1 = bounds.topleft
        x2, y2 = bounds.bottomright

        cells = []
        for x in range(x1 // self.cell_size, x2 // self.cell_size + 1):
            for y in range(y1 // self.cell_size, y2 // self.cell_size + 1):
                cells.append((x, y))
        return cells

    def add(self, game_object: GameObject) -> None:
        """
        Adds a game object to the grid.

        Args:
            game_object (GameObject): The game object to add.
        """
        for cell in self.get_cell_coords(game_object.bounds):
            if cell not in self.m_grid:
                self.m_grid[cell] = []
            self.m_grid[cell].append(game_object)

    def get_nearby(self, game_object: GameObject) -> list[GameObject]:
        """
        Gets a list of game objects that are in the cells nearby the given game object.

        Args:
            game_object (GameObject): The game object to query for nearby objects.

        Returns:
            list[GameObject]: A list of nearby game objects.
        """
        nearby = set()  # use a set in order to avoid duplicates
        for cell in self.get_cell_coords(game_object.bounds):
            if cell in self.m_grid:
                nearby.update(self.m_grid[cell])
        return list(nearby)  # convert set to list and return it

    def clear(self) -> None:
        """
        Clears all objects from the grid.
        """
        self.m_grid.clear()
