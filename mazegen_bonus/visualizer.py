#!/usr/bin/env python3

import os
import time
from typing import List, Tuple, Optional

from .maze import Maze
from .maze_generator import MazeGenerator
from .parser import Parsing


class MazeRenderer:
    """
    Simple terminal maze renderer with ANSI colors and keyboard interaction.
    """

    # color codes
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bg_black': '\033[40m',
        'bg_red': '\033[41m',
        'bg_green': '\033[42m',
        'bg_yellow': '\033[43m',
        'bg_blue': '\033[44m',
        'bg_magenta': '\033[45m',
        'bg_cyan': '\033[46m',
        'bg_white': '\033[47m',
        'bold': '\033[1m',
    }

    # Color themes (wall, path, entry, exit, pattern)
    THEMES = [
        # wall, path, entry, exit, pattern
        ('cyan', 'green', 'red', 'magenta', 'yellow'),
        ('white', 'blue', 'red', 'yellow', 'cyan'),
        ('yellow', 'green', 'magenta', 'red', 'blue'),
        ('magenta', 'cyan', 'green', 'yellow', 'red'),
    ]

    def __init__(self, maze: Maze, generator: MazeGenerator, config: Parsing):
        self.maze = maze
        self.generator = generator
        self.config = config
        self.show_path = True
        self.theme_idx = 0
        self._path_cells: Optional[List[Tuple[int, int]]] = None

    def _get_path_cells(self) -> List[Tuple[int, int]]:
        """
        Return list of (x, y) coordinates on the shortest path
        from entry to exit.
        """
        if self._path_cells is None:
            path_str = self.maze\
                        .find_shortest_path(self.maze.entry, self.maze.exit)
            if not path_str:
                self._path_cells = []
                return self._path_cells
            x, y = self.maze.entry
            cells = [(x, y)]
            for move in path_str:
                if move == 'N':
                    y -= 1
                elif move == 'S':
                    y += 1
                elif move == 'E':
                    x += 1
                elif move == 'W':
                    x -= 1
                cells.append((x, y))
            self._path_cells = cells
        return self._path_cells

    def _color(self, name: str) -> str:
        """Return ANSI code for given color name."""
        return self.COLORS.get(name, '')

    def _render_cell(self, x: int, y: int) -> str:
        """Return colored representation of a single cell."""
        cell = self.maze.get_cell(x, y)
        theme = self.THEMES[self.theme_idx]
        wall_color, path_color, entry_color, exit_color, pattern_color = theme

        # Determine content
        if (x, y) == self.maze.entry:
            content = 'E'
            color = entry_color
        elif (x, y) == self.maze.exit:
            content = 'X'
            color = exit_color
        elif cell.protected:
            content = '█'  # solid block for "42" pattern
            color = pattern_color
        else:
            content = ' '  # empty space for open cell
            color = 'reset'

            if self.show_path and (x, y) in self._get_path_cells():
                color = path_color
                content = '●'

        # Build the cell display (3 characters wide for spacing)
        colored = f"{self._color(color)}{content}{self._color('reset')}"
        return f" {colored} "

    def _render_wall_horizontal(self, y: int) -> str:
        """Return the horizontal wall line above row y."""
        # theme = self.THEMES[self.theme_idx]
        # wall_color = theme[0]
        line = "+"
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)
            line += "---" if cell.has_wall('N') else "   "
            line += "+"
        # return f"{self._color(wall_color)}{line}{self._color('reset')}"
        return line

    def _render_wall_vertical(self, y: int) -> str:
        """Return the vertical wall line for row y (cells + east walls)"""
        # theme = self.THEMES[self.theme_idx]
        # wall_color = theme[0]
        line = ""
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)
            line += "|" if cell.has_wall('W') else " "
            line += self._render_cell(x, y)
        # Last east wall
        last_cell = self.maze.get_cell(self.maze.width - 1, y)
        line += "|" if last_cell.has_wall('E') else " "
        # return f"{self._color(wall_color)}{line}{self._color('reset')}"
        return line

    def render(self) -> str:
        """Return the full ASCII representation of the maze with colors"""
        # theme = self.THEMES[self.theme_idx]
        # wall_color = theme[0]
        lines = []
        # Top border
        lines.append(self._render_wall_horizontal(0))
        for y in range(self.maze.height):
            # Cells + vertical walls
            lines.append(self._render_wall_vertical(y))
            # Bottom wall of this row (or south wall)
            if y < self.maze.height - 1:
                lines.append(self._render_wall_horizontal(y + 1))
            else:
                # Last row: south border
                bottom = "+"
                for x in range(self.maze.width):
                    cell = self.maze.get_cell(x, y)
                    bottom += "---" if cell.has_wall('S') else "   "
                    bottom += "+"
                lines.append(bottom)

        return "\n".join(lines)

    def clear_screen(self) -> None:
        """Clear terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_help(self) -> None:
        """Display interactive commands."""
        print("\n" + "=" * 50)
        print("Commands:")
        print("  r - Regenerate maze")
        print("  p - Show/hide shortest path")
        print("  c - Change colors")
        print("  q - Quit")
        print("=" * 50)

    def regenerate(self) -> None:
        """
        Generate a new maze with same config.
        Re-create maze and generator
        """
        new_maze = Maze(self.config)
        # new_maze.seed = random.randrange(50)
        new_maze.apply_42_pattern()
        new_gen = MazeGenerator(new_maze)
        new_gen.generate()
        if not new_maze.validate():
            print("Warning: regenerated maze is invalid, keeping previous.")
            return
        self.maze = new_maze
        self.generator = new_gen
        self._path_cells = None

    def run(self) -> None:
        """Start interactive display loop"""
        self.clear_screen()
        while True:
            print(self.render())
            self.show_help()
            key = input("> ").strip().lower()
            if key == 'q':
                break
            elif key == 'r':
                self.regenerate()
                self.clear_screen()
            elif key == 'p':
                self.show_path = not self.show_path
                self.clear_screen()
            elif key == 'c':
                self.theme_idx = (self.theme_idx + 1) % len(self.THEMES)
                self.clear_screen()
            else:
                self.clear_screen()
                print("Unknown command. Use r, p, c, q.")
                time.sleep(1)
                self.clear_screen()


if __name__ == '__main__':
    try:
        parser = Parsing("config.txt")
        parser.parse()
        maze = Maze(parser)
        maze.apply_42_pattern()

        generator = MazeGenerator(maze)
        generator.generate()

        renderer = MazeRenderer(generator.maze, generator, parser)
        renderer.run()
    except Exception as e:
        print(
            f"Caught an error: {e}"
        )
        exit()
