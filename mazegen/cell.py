class Cell():
    """
    Represents a single cell in a maze grid.

    A cell has four walls (north, east, south, west) that can be broken
    to create paths.
    Each cell tracks its position in the grid and whether it has been visited.
    """

    def __init__(self, x: int, y: int, north: int = 1, east: int = 1,
                 south: int = 1, west: int = 1):
        self._north = north
        self._east = east
        self._south = south
        self._west = west
        self._x = x
        self._y = y
        self.visited = False

    def break_wall(self, direction: str) -> None:
        """
        Break the wall in the specified direction.
        """

        if direction == "north":
            self._north = 0
        elif direction == "east":
            self._east = 0
        elif direction == "south":
            self._south = 0
        elif direction == "west":
            self._west = 0

    def get_direction(self, direction: str) -> int:
        """
        Get the wall state in the specified direction.
        Returns:
            The wall state (1 = wall present, 0 = wall broken).
        """
        if direction == "north":
            return self._north
        elif direction == "east":
            return self._east
        elif direction == "south":
            return self._south
        else:
            return self._west

    def get_coord(self, pos: str) -> int:
        """
        Get the coordinate value of the cell.
        """

        if pos == 'x':
            return self._x
        else:
            return self._y

    def get_visit(self) -> bool:
        """
        Check if the cell has been visited.
        """
        return self.visited

    def set_visit(self) -> None:
        """
        Mark the cell as visited.
        """
        self.visited = True
