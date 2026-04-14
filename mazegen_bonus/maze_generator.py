#!/usr/bin/env python3

import random
from typing import List, Tuple, Set
from .maze import Maze
from .parser import Parsing


class MazeGenerator:
    """Generate a maze from a Maze instance.

    This class applies the maze generation algorithm while preserving any
    protected cells used to draw the visible "42" pattern required by the
    subject. It supports both perfect and non-perfect mazes depending on
    the maze configuration.
    """
    def __init__(self, maze: Maze) -> None:
        """Initialize the generator with a maze object.

        Args:
            maze: A Maze instance already configured with dimensions, entry,
                exit, and optional protected cells.

        If a seed is defined in the maze configuration, it is used to make
        generation reproducible.
        """
        self.maze = maze
        # if maze.seed is not None:
        #     random.seed(maze.seed)

        # Mark protected cells (all walls = 1, check individual walls)
        self._protected_cells: Set[Tuple[int, int]] = set()
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                # if all(cell.has_wall(d) for d in ['N', 'E', 'S', 'W']):
                if cell.protected:
                    self._protected_cells.add((x, y))

    def generate(self) -> None:
        """Generate the maze structure in place.

        This method starts from the entry cell, carves passages recursively,
        and optionally adds extra openings when the maze is not required to be
        perfect.

        Protected cells are excluded from carving so the "42" pattern remains
        fully closed and visible.
        """
        visited = [[False] * self.maze.width for _ in range(self.maze.height)]
        for (x, y) in self._protected_cells:
            visited[y][x] = True

        self._carve_passages(self.maze.entry[0], self.maze.entry[1], visited)

        if not self.maze.perfect:
            self._add_extra_passages()

    def _carve_passages(self,
                        x: int,
                        y: int,
                        visited: List[List[bool]]) -> None:
        """Recursively carve passages using randomized depth-first search.

        Args:
            x: X coordinate of the current cell.
            y: Y coordinate of the current cell.
            visited: 2D matrix tracking which cells have already been visited.

        A passage is only kept if it does not violate the subject rule that
        forbids large open areas. Protected cells are never opened.
        """
        visited[y][x] = True
        dirs = ['N', 'E', 'S', 'W']
        random.shuffle(dirs)

        for direction in dirs:
            neighbor = self.maze.get_neighbors_in_direction(x, y, direction)
            if neighbor is None:
                continue
            nx, ny = neighbor
            if visited[ny][nx]:
                continue
            if (nx, ny) in self._protected_cells:
                continue

            self.maze.remove_wall_between((x, y), (nx, ny))

            if self.maze.has_no_large_openings():
                self._carve_passages(nx, ny, visited)
            else:
                self.maze.add_wall_between((x, y), (nx, ny))

    def _add_extra_passages(self) -> None:
        """Open additional walls to create a non-perfect maze.

        This method selects candidate internal walls between non-protected
        neighboring cells and removes some of them to introduce multiple paths.
        """

        walls: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (x, y) in self._protected_cells:
                    continue

                for direction in ['E', 'S']:
                    neighbor = self.maze\
                                .get_neighbors_in_direction(x, y, direction)
                    if neighbor is None:
                        continue
                    if neighbor in self._protected_cells:
                        continue
                    if self.maze.get_cell(x, y).has_wall(direction):
                        walls.append(((x, y), neighbor))

        if not walls:
            return

        random.shuffle(walls)
        num_to_open = max(1, len(walls) // 5)

        opened = 0
        for c1, c2 in walls:
            if opened >= num_to_open:
                break

            self.maze.remove_wall_between(c1, c2)

            if self.maze.has_no_large_openings():
                opened += 1
            else:
                self.maze.add_wall_between(c1, c2)


if __name__ == '__main__':
    parser = Parsing("config.txt")
    parser.parse()
    maze = Maze(parser)
    maze.apply_42_pattern()
    generator = MazeGenerator(maze)
    generator.generate()
    output = maze.to_hex_output()
    # print(generator._protected_cells)
    print(generator.maze)
    print(output)
