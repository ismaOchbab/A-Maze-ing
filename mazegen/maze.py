#!/usr/bin/env python3

from cell import Cell
from parser import Parsing
from typing import List, Tuple, Optional, Deque
from collections import deque


class Maze:
    """
    represents a complete maze structure with walls and paths
    """
    def __init__(self, config: Parsing) -> None:
        """
        Initialize a maze using a validated config object
        """
        self.width = config.width
        self.height = config.height
        self.entry = (config.entry['x'], config.entry['y'])
        self.exit = (config.exit['x'], config.exit['y'])
        self.perfect = config.perfect
        self.seed = config.seed
        self.extra = config.extra
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(self.width)] for _ in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Returns the cell at coordinates (x, y)
        """
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, cell: Cell) -> None:
        """
        Set the cell at (x,y)
        """
        self.grid[y][x] = cell

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Returns list of (nx, ny) for all cardinal neighbors that exist
        Order: North, East, South, West
        """
        neighbors = []
        if y > 0:
            neighbors.append((x, y - 1))  # North
        if x < self.width - 1:
            neighbors.append((x + 1, y))
        if y < self.height - 1:
            neighbors.append((x, y + 1))
        if x > 0:
            neighbors.append((x - 1, y))
        return neighbors

    def get_neighbors_in_direction(
            self,
            x: int,
            y: int,
            direction: str) -> Optional[Tuple[int, int]]:
        """
        Returns neighbor coordinates in given direction
        Returns None if that neighbor is out of bounds
        """
        if direction == 'N' and y > 0:
            return (x, y - 1)
        if direction == 'E' and x < self.width - 1:
            return (x + 1, y)
        if direction == 'S' and y < self.height - 1:
            return (x, y + 1)
        if direction == 'W' and x > 0:
            return (x - 1, y)
        return None

    def remove_wall_between(self,
                            cell1: Tuple[int, int],
                            cell2: Tuple[int, int]) -> None:
        """
        Removes the wall between two adjacent cells (both direction)
        Assumes cell1 and cell2 are neighbors
        """
        x1, y1 = cell1
        x2, y2 = cell2
        if x2 == x1 + 1 and y2 == y1:
            self.get_cell(x1, y1).remove_wall('E')
            self.get_cell(x2, y2).remove_wall('W')
        elif x2 == x1 - 1 and y2 == y1:
            self.get_cell(x1, y1).remove_wall('W')
            self.get_cell(x2, y2).remove_wall('E')
        elif y2 == y1 + 1 and x2 == x1:
            self.get_cell(x1, y1).remove_wall('S')
            self.get_cell(x2, y2).remove_wall('N')
        elif y2 == y1 - 1 and x2 == x1:
            self.get_cell(x1, y1).remove_wall('N')
            self.get_cell(x2, y2).remove_wall('S')
        else:
            raise ValueError("Cells are not adjacent")

    def add_wall_between(self,
                         cell1: Tuple[int, int],
                         cell2: Tuple[int, int]) -> None:
        x1, y1 = cell1
        x2, y2 = cell2

        if x2 == x1 + 1 and y2 == y1:
            self.get_cell(x1, y1).add_wall('E')
            self.get_cell(x2, y2).add_wall('W')
        elif x2 == x1 - 1 and y2 == y1:
            self.get_cell(x1, y1).add_wall('W')
            self.get_cell(x2, y2).add_wall('E')
        elif y2 == y1 + 1 and x2 == x1:
            self.get_cell(x1, y1).add_wall('S')
            self.get_cell(x2, y2).add_wall('N')
        elif y2 == y1 - 1 and x2 == x1:
            self.get_cell(x1, y1).add_wall('N')
            self.get_cell(x2, y2).add_wall('S')
        else:
            raise ValueError("Cells are not adjacent")

    # Post generation verifications
    def _border_walls_valid(self) -> bool:
        """
        Checks that all border cells have their outer walls closed
        except at entry and exit
        """
        for x in range(self.width):
            if not self.get_cell(x, 0).has_wall('N'):
                return False
            if not self.get_cell(x, self.height - 1).has_wall('S'):
                return False

        for y in range(self.height):
            if not self.get_cell(0, y).has_wall('W'):
                return False
            if not self.get_cell(self.width - 1, y).has_wall('E'):
                return False
        return True

    def is_fully_connected(self) -> bool:
        """
        Checks if all cells are reachable from the entry
        """
        if self.width == 0 or self.height == 0:
            return False
        if self.get_cell(*self.entry).protected\
                or self.get_cell(*self.exit).protected:
            return False

        visited = [[False] * self.width for _ in range(self.height)]
        queue: Deque[Tuple[int, int]] = deque()
        queue.append(self.entry)
        visited[self.entry[1]][self.entry[0]] = True

        while queue:
            x, y = queue.popleft()
            for direction in ['N', 'E', 'S', 'W']:
                nx, ny = x, y
                if direction == 'N' and y > 0\
                        and not self.get_cell(x, y).has_wall('N'):
                    nx, ny = x, y - 1
                elif direction == 'E' and x < self.width - 1\
                        and not self.get_cell(x, y).has_wall('E'):
                    nx, ny = x + 1, y
                elif direction == 'S' and y < self.height - 1\
                        and not self.get_cell(x, y).has_wall('S'):
                    nx, ny = x, y + 1
                elif direction == 'W' and x > 0\
                        and not self.get_cell(x, y).has_wall('W'):
                    nx, ny = x - 1, y
                else:
                    continue

                if self.get_cell(nx, ny).protected:
                    continue

                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny))

        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y).protected:
                    continue
                if not visited[y][x]:
                    return False
        return True

    def walls_coherence(self) -> bool:
        """
        checks that neighboring cells have matching walls
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                # east vs west of east neighbour
                if x < self.width - 1:
                    east_cell = self.get_cell(x + 1, y)
                    if cell.has_wall('E') != east_cell.has_wall('W'):
                        return False
                # south vs north of south neighbour
                if y < self.height - 1:
                    south_cell = self.get_cell(x, y + 1)
                    if cell.has_wall('S') != south_cell.has_wall('N'):
                        return False
        return True

    def has_no_large_openings(self) -> bool:
        """
        checks no 3x3 area exists where all interior walls are absent
        """
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                # horizontal internal walls between columns
                open_area = True
                for dy in range(3):
                    for dx in range(2):
                        cell_left = self.get_cell(x + dx, y + dy)
                        if cell_left.has_wall('E'):
                            open_area = False
                            break
                    if not open_area:
                        break
                if not open_area:
                    continue
                # vertical internal walls between rows
                for dx in range(3):
                    for dy in range(2):
                        cell_top = self.get_cell(x + dx, y + dy)
                        if cell_top.has_wall('S'):
                            open_area = False
                            break
                    if not open_area:
                        break
                if open_area:
                    return False
        return True

    # validates all the checks funcs
    def validate(self) -> bool:
        """
        Subject-level validation.
        """
        if not self._border_walls_valid():
            return False
        if not self.walls_coherence():
            return False
        if not self.has_no_large_openings():
            return False
        if not self.is_fully_connected():
            return False
        if self.find_shortest_path(self.entry, self.exit) == "":
            return self.entry == self.exit
        return True

    # 42 pattern (to be called by the generator)
    def apply_42_pattern(self) -> bool:
        """
        Draw the visible '42' as protected fully-closed cells.
        Returns False if the maze is too small.
        """
        pattern_4 = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]
        pattern_2 = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]

        # width = 3 + 1 gap + 3 = 7
        if self.width < 7 or self.height < 5:
            print("Warning: maze too small to place the '42' pattern.")
            return False

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        protected_positions = set()

        for dy in range(5):
            for dx in range(3):
                if pattern_4[dy][dx] == 1:
                    protected_positions.add((start_x + dx, start_y + dy))
                if pattern_2[dy][dx] == 1:
                    protected_positions.add((start_x + 4 + dx, start_y + dy))

        if self.entry in protected_positions\
                or self.exit in protected_positions:
            print(
                "Warning: 42 pattern overlaps entry or exit, pattern omitted.")
            return False

        for x, y in protected_positions:
            cell = self.get_cell(x, y)
            cell.protected = True
            for direction in ['N', 'E', 'S', 'W']:
                cell.set_direction(direction, 1)

        return True

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
                if direction == 'N' and y > 0\
                        and not self.get_cell(x, y).has_wall('N'):
                    nx, ny = x, y - 1
                elif direction == 'E' and x < self.width - 1\
                        and not self.get_cell(x, y).has_wall('E'):
                    nx, ny = x + 1, y
                elif direction == 'S' and y < self.height - 1\
                        and not self.get_cell(x, y).has_wall('S'):
                    nx, ny = x, y + 1
                elif direction == 'W' and x > 0\
                        and not self.get_cell(x, y).has_wall('W'):
                    nx, ny = x - 1, y
                else:
                    continue

                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny, path + direction))

        # No path found
        return ""

    def to_hex_output(self) -> str:
        """
        converts maze to the required output file format
        """
        lines = []
        for y in range(self.height):
            row_hex = ''.join(self.get_cell(x, y).get_hex_value()
                              for x in range(self.width))
            lines.append(row_hex)
        lines.append('')
        lines.append(f"{self.entry[0]}, {self.entry[1]}")
        lines.append(f"{self.exit[0]}, {self.exit[1]}")
        path = self.find_shortest_path(self.entry, self.exit)
        lines.append(path)
        return '\n'.join(lines)

    def __repr__(self) -> str:
        """
        ASCII representation of the maze
        E = entry, X = exit
        """
        if self.width == 0 or self.height == 0:
            return ""

        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                cell = self.get_cell(x, y)
                line += "+" + ("---" if cell.has_wall('N') else "   ")
            line += "+"
            lines.append(line)

            line = ""
            for x in range(self.width):
                cell = self.get_cell(x, y)
                line += "|" if cell.has_wall('W') else " "
                if (x, y) == self.entry:
                    line += " E "
                elif (x, y) == self.exit:
                    line += " X "
                elif cell.protected:
                    line += " @ "
                else:
                    line += "   "

            last_cell = self.get_cell(self.width - 1, y)
            line += "|" if last_cell.has_wall('E') else " "
            lines.append(line)

        last_row = self.height - 1
        line = ""
        for x in range(self.width):
            cell = self.get_cell(x, last_row)
            line += "+" + ("---" if cell.has_wall('S') else "   ")
        line += "+"
        lines.append(line)

        return "\n".join(lines)


if __name__ == '__main__':

    try:
        config = Parsing("config.txt")
        config.parse()
        maze = Maze(config=config)
        maze.apply_42_pattern()
        print(maze)
        print()
        print(maze.to_hex_output())
    except Exception as e:
        print(f"Caught an error: {e}")
        exit()
