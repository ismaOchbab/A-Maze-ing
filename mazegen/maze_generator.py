import random
import os
from .cell import Cell
from .maze import Maze
from .visualizer import MazeRenderer
import time


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int | None = None):
        self.maze = maze
        if seed is not None:
            random.seed(seed)

    def check_neighbour(self, cell: Cell) -> list[Cell]:
        x = cell.get_coord('x')
        y = cell.get_coord('y')
        neighbour: list[Cell] = []
        if (y + 1 < self.maze.height and
           self.maze.grid[y + 1][x].visited is False):
            neighbour.append(self.maze.grid[y + 1][x])
        if y - 1 >= 0 and self.maze.grid[y - 1][x].visited is False:
            neighbour.append(self.maze.grid[y - 1][x])
        if (x + 1 < self.maze.width and
           self.maze.grid[y][x + 1].visited is False):
            neighbour.append(self.maze.grid[y][x + 1])
        if x - 1 >= 0 and self.maze.grid[y][x - 1].visited is False:
            neighbour.append(self.maze.grid[y][x - 1])
        return neighbour

    def def_direction(self, cell1: Cell, cell2: Cell) -> None:
        x3 = cell1.get_coord('x') - cell2.get_coord('x')
        y3 = cell1.get_coord('y') - cell2.get_coord('y')
        if x3 > 0:
            cell1.break_wall("west")
            cell2.break_wall("east")
        elif x3 < 0:
            cell1.break_wall("east")
            cell2.break_wall("west")
        elif y3 > 0:
            cell1.break_wall("north")
            cell2.break_wall("south")
        else:
            cell1.break_wall("south")
            cell2.break_wall("north")

    def generate(self, perfect: bool = True,
                 renderer: MazeRenderer | None = None,
                 index: int = 0) -> None:
        stack: list[Cell] = []
        stack.append(self.maze.grid[0][0])
        self.maze.grid[0][0].set_visit()
        if self.maze.width > 8 and self.maze.height > 7:
            pat_42 = self.maze.pattern_42()
            for cell in pat_42:
                cell.set_visit()
        else:
            print("Warning: Maze too small to render the '42' pattern\n")
        while (len(stack) != 0):
            neighbour = self.check_neighbour(stack[-1])
            if len(neighbour) != 0:
                next_cell = random.choice(neighbour)
                self.def_direction(stack[-1], next_cell)
                next_cell.set_visit()
                stack.append(next_cell)

                if renderer:
                    os.system('clear')
                    renderer.display(False, index)
                    time.sleep(0.01)
            else:
                stack.pop()

        if perfect is False:
            self.make_imperfect()

    def _is_3x3_open(self, start_x: int, start_y: int,
                     c1: Cell, c2: Cell) -> bool:
        """Vérifie si une zone 3x3 spécifique est totalement ouverte"""
        for dy in range(3):
            for dx in range(3):
                cx = start_x + dx
                cy = start_y + dy
                c = self.maze.get_cell(cx, cy)

                if dx < 2:
                    c_east = self.maze.get_cell(cx + 1, cy)
                    is_the_broken_wall = ((c == c1 and c_east == c2) or
                                          (c == c2 and c_east == c1))
                    if not is_the_broken_wall and c.get_direction("east") == 1:
                        return False

                if dy < 2:
                    c_south = self.maze.get_cell(cx, cy + 1)
                    is_the_broken_wall = ((c == c1 and c_south == c2) or
                                          (c == c2 and c_south == c1))
                    if (not is_the_broken_wall
                       and c.get_direction("south") == 1):
                        return False
        return True

    def _would_form_3x3(self, c1: Cell, c2: Cell) -> bool:
        'Vérifie si casser le mur entre c1 et '
        'c2 créerait une zone ouverte de 3x3'
        x1, y1 = c1.get_coord('x'), c1.get_coord('y')
        x2, y2 = c2.get_coord('x'), c2.get_coord('y')

        min_x = max(0, min(x1, x2) - 2)
        max_x = min(self.maze.width - 3, max(x1, x2))
        min_y = max(0, min(y1, y2) - 2)
        max_y = min(self.maze.height - 3, max(y1, y2))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self._is_3x3_open(x, y, c1, c2):
                    return True
        return False

    def make_imperfect(self) -> None:
        'Logique du Projet 1 : casse environ 20% des murs restants au hasard'
        pat_42 = []
        if self.maze.width > 8 and self.maze.height > 7:
            pat_42 = self.maze.pattern_42()

        walls_to_break: list[tuple[Cell, Cell]] = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                current = self.maze.get_cell(x, y)

                if current in pat_42:
                    continue

                if x + 1 < self.maze.width:
                    east_neighbor = self.maze.get_cell(x + 1, y)
                    if (east_neighbor not in pat_42
                       and current.get_direction("east") == 1):
                        walls_to_break.append((current, east_neighbor))

                if y + 1 < self.maze.height:
                    south_neighbor = self.maze.get_cell(x, y + 1)
                    if (south_neighbor not in pat_42 and
                       current.get_direction("south") == 1):
                        walls_to_break.append((current, south_neighbor))

        if not walls_to_break:
            return

        random.shuffle(walls_to_break)
        num_to_open = max(1, len(walls_to_break) // 5)
        opened = 0

        for c1, c2 in walls_to_break:
            if opened >= num_to_open:
                break

            if not self._would_form_3x3(c1, c2):
                self.def_direction(c1, c2)
                opened += 1
