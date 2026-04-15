from .cell import Cell
from collections import deque
from typing import Tuple, Deque


class Maze:
    """
        Represents a maze grid composed of cells.

        A Maze is a rectangular grid of cells with defined
        entry and exit points.
        It manages the maze structure, pathfinding,
        and can output the maze in various formats.
    """
    def __init__(self, width: int, height: int, output: str,
                 entry: dict[str, int], exit: dict[str, int]):
        """
        Initialize a new Maze.

        Args:
            width: The width of the maze (number of columns).
            height: The height of the maze (number of rows).
            output: The file path where the maze output will be written.
            entry: A dictionary with 'x' and 'y' coordinates
            for the entry point.
            exit: A dictionary with 'x' and 'y' coordinates for the exit point.
        """

        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self._output = output
        self.grid: list[list[Cell]] = self._create_empty_grid()

    def _create_empty_grid(self) -> list[list[Cell]]:
        """
        Create an empty grid of cells for the maze.

        Returns:
            A 2D list of Cell objects representing the maze grid.
        """
        grid: list[list[Cell]] = []
        for i in range(0, self.height):
            grid.append([])
            for j in range(0, self.width):
                grid[i].append(Cell(j, i))
        return grid

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Retrieve a cell at the specified coordinates.

        Args:
            x: The x-coordinate (column) of the cell.
            y: The y-coordinate (row) of the cell.

        Returns:
            The Cell object at the given coordinates.
        """
        return self.grid[y][x]

    def pattern_42(self) -> list[Cell]:
        """
        Generate the 42 pattern - a special decorative pattern in the maze.

        The pattern is centered in the maze and forms the number 42.

        Returns:
            A list of cells that make up the 42 pattern.
        """
        mid_x = self.width // 2
        mid_y = self.height // 2
        offsets = [
            (-3, -2),
            (-3, -1),
            (-3,  0), (-2,  0), (-1,  0),
                                (-1,  1),
                                (-1,  2),

            (1, -2), (2, -2), (3, -2),
                              (3, -1),
            (1,  0), (2,  0), (3,  0),
            (1,  1),
            (1,  2), (2,  2), (3,  2)
        ]
        pat_42: list[Cell] = []
        for dx, dy in offsets:
            x = mid_x + dx
            y = mid_y + dy
            pat_42.append(self.grid[y][x])
        return pat_42

    def check_wall(self, cell: Cell) -> list[Cell]:
        """
        Get all neighboring cells accessible through broken walls.

        Args:
            cell: The cell to check neighbors for.

        Returns:
            A list of neighboring cells that are reachable (walls are broken).
        """
        x = cell.get_coord('x')
        y = cell.get_coord('y')
        neighbour: list[Cell] = []
        if cell.get_direction("north") == 0:
            neighbour.append(self.grid[y - 1][x])
        if cell.get_direction("east") == 0:
            neighbour.append(self.grid[y][x + 1])
        if cell.get_direction("west") == 0:
            neighbour.append(self.grid[y][x - 1])
        if cell.get_direction("south") == 0:
            neighbour.append(self.grid[y + 1][x])
        return neighbour

    def find_shortest_path(self,
                           start: Tuple[int, int],
                           end: Tuple[int, int]) -> str:
        """
        returns shortest path from start to end as a string of moves (N,E,S,W)
        uses BFS. returns empty string if start == end
        """
        if start == end:
            return ""

        queue: Deque[Tuple[int, int, str]] = deque()
        visited = [[False] * self.width for _ in range(self.height)]

        queue.append((start[0], start[1], ""))
        visited[start[1]][start[0]] = True

        while queue:
            x, y, path = queue.popleft()
            if (x, y) == end:
                return path

            for direction in ['N', 'E', 'S', 'W']:
                nx, ny = x, y
                if (direction == 'N'
                    and y > 0
                   and not self.get_cell(x, y).get_direction('north') == 1):
                    nx, ny = x, y - 1
                elif direction == 'E' and x < self.width - 1\
                        and not self.get_cell(x, y).get_direction('east') == 1:
                    nx, ny = x + 1, y
                elif (direction == 'S'
                      and y < self.height - 1
                      and not self.get_cell(x, y).get_direction('south') == 1):
                    nx, ny = x, y + 1
                elif direction == 'W' and x > 0\
                        and not self.get_cell(x, y).get_direction('west') == 1:
                    nx, ny = x - 1, y
                else:
                    continue

                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny, path + direction))

        # No path found
        return ""

    def hex_dir(self, c1: Cell, c2: Cell) -> str:
        """
        Determine the direction from cell c1 to cell c2.

        Args:
            c1: The first cell.
            c2: The second cell.

        Returns:
            A string representing the direction: 'W' (west), 'E' (east),
            'N' (north), or 'S' (south).
        """
        x1, x2 = c1.get_coord('x'), c2.get_coord('x')
        y1, y2 = c1.get_coord('y'), c2.get_coord('y')
        if x1 - x2 > 0:
            return "W"
        elif x1 - x2 < 0:
            return "E"
        elif y1 - y2 > 0:
            return "N"
        else:
            return "S"

    def hexa_output(self) -> None:
        """
        Output the maze in hexadecimal format to the specified output file.

        The output format includes:
        - Each cell's wall configuration in hexadecimal (0-F)
        - Entry point coordinates
        - Exit point coordinates
        - Shortest path from entry to exit as a sequence of moves (N, E, S, W)
        """
        line = ""
        for c in self.grid:
            for i in range(0, self.width):
                value = 0
                if c[i].get_direction("north") == 1:
                    value += 1
                if c[i].get_direction("east") == 1:
                    value += 2
                if c[i].get_direction("south") == 1:
                    value += 4
                if c[i].get_direction("west") == 1:
                    value += 8
                line += f"{value:X}"
            line += "\n"
        line += "\n"
        line += f"{self.entry['x']},{self.entry['y']}\n"
        line += f"{self.exit['x']},{self.exit['y']}\n"
        path = self.find_shortest_path((self.entry['x'], self.entry['y']),
                                       (self.exit['x'], self.exit['y']))
        line += (path)
        with open(self._output, 'w') as file:
            file.write(line)
            file.close()
