# mazegen/generator.py
import random
from typing import List, Tuple, Optional, Set
from maze import Maze
from cell import Cell
from parser import Parsing


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        if maze.seed is not None:
            random.seed(maze.seed)
        
        # Mark protected cells (all walls = 1, check individual walls)
        self._protected_cells: Set[Tuple[int, int]] = set()
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                # if all(cell.has_wall(d) for d in ['N', 'E', 'S', 'W']):
                if cell.protected:
                    self._protected_cells.add((x, y))

    def generate(self) -> None:
        visited = [[False] * self.maze.width for _ in range(self.maze.height)]
        for (x, y) in self._protected_cells:
            visited[y][x] = True
        
        self._carve_passages(self.maze.entry[0], self.maze.entry[1], visited)
        
        if not self.maze.perfect:
            self._add_extra_passages()

    def _carve_passages(self, x: int, y: int, visited: List[List[bool]]) -> None:
        visited[y][x] = True
        dirs = ['N', 'E', 'S', 'W']
        random.shuffle(dirs)
        
        for direction in dirs:
            neighbor = self.maze.get_neighbors_in_direction(x, y, direction)
            if not neighbor:
                continue
            nx, ny = neighbor
            if visited[ny][nx] or (nx, ny) in self._protected_cells:
                continue
            
            # Save state before modification
            cell1 = self.maze.get_cell(x, y)
            cell2 = self.maze.get_cell(nx, ny)
            old_walls1 = {d: cell1.has_wall(d) for d in ['N', 'E', 'S', 'W']}
            old_walls2 = {d: cell2.has_wall(d) for d in ['N', 'E', 'S', 'W']}
            
            # Remove wall
            self.maze.remove_wall_between((x, y), (nx, ny))
            
            if self.maze.has_no_large_openings():
                self._carve_passages(nx, ny, visited)
            else:
                # Restore walls
                for d in ['N', 'E', 'S', 'W']:
                    if old_walls1[d]:
                        cell1.add_wall(d)
                    if old_walls2[d]:
                        cell2.add_wall(d)

    def _add_extra_passages(self) -> None:
        walls = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (x, y) in self._protected_cells:
                    continue
                for direction in ['E', 'S']:
                    neighbor = self.maze.get_neighbors_in_direction(x, y, direction)
                    if neighbor:
                        nx, ny = neighbor
                        if (nx, ny) not in self._protected_cells:
                            cell = self.maze.get_cell(x, y)
                            if cell.has_wall(direction):
                                walls.append(((x, y), neighbor, direction))
        
        num_to_open = max(1, len(walls) // 5)
        random.shuffle(walls)
        
        for (c1, c2, _) in walls[:num_to_open]:
            self.maze.remove_wall_between(c1, c2)
            if not self.maze.has_no_large_openings():
                self.maze.remove_wall_between(c1, c2)  # undo


parser = Parsing("config.txt")
parser.parse()
maze = Maze(parser)
maze.apply_42_pattern()
generator = MazeGenerator(maze)
generator.generate()
output = maze.to_hex_output()
print(generator._protected_cells)
print(generator.maze)
# print(output)