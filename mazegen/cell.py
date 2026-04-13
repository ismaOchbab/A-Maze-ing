class Cell():
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
        if direction == "north":
            self._north = 0
        elif direction == "east":
            self._east = 0
        elif direction == "south":
            self._south = 0
        elif direction == "west":
            self._west = 0

    def get_direction(self, direction: str) -> int:
        if direction == "north":
            return self._north
        elif direction == "east":
            return self._east
        elif direction == "south":
            return self._south
        else:
            return self._west

    def get_coord(self, pos: str) -> int:
        if pos == 'x':
            return self._x
        else:
            return self._y

    def get_visit(self) -> bool:
        return self.visited

    def set_visit(self) -> None:
        self.visited = True
