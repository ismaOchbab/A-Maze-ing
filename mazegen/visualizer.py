from .cell import Cell
from .maze import Maze


class MazeRenderer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def color_42(self, grid: list[list[str]], pat_42: list[Cell]) -> None:
        for c in self.maze.grid:
            for i in range(0, self.maze.width):
                cx = (c[i].get_coord('x') * 2) + 1
                cy = (c[i].get_coord('y') * 2) + 1
                if c[i] in pat_42:
                    grid[cy][cx] = f"{"\033[100m"}   {"\033[0m"}"

    def _get_path_cells(self) -> list[Cell]:
        """
        Convertit la chaîne de direction ("EESSW...") en une liste d'objets
        Cell pour que le display puisse les utiliser.
        """
        # 1. On récupère le string ("ESSEE...") via le BFS
        path_str = self.maze.find_shortest_path(
            (self.maze.entry['x'], self.maze.entry['y']),
            (self.maze.exit['x'], self.maze.exit['y'])
        )

        if not path_str:
            return []

        # 2. On commence aux coordonnées de l'entrée
        x = self.maze.entry['x']
        y = self.maze.entry['y']

        # 3. On initialise la liste avec la Cellule de départ
        cells = [self.maze.get_cell(x, y)]

        # 4. On lit chaque lettre, on avance,
        # et on attrape la Cell correspondante
        for move in path_str:
            if move == 'N':
                y -= 1
            elif move == 'S':
                y += 1
            elif move == 'E':
                x += 1
            elif move == 'W':
                x -= 1

            cells.append(self.maze.get_cell(x, y))

        return cells

    def display(self, show_path: bool, index: int) -> None:
        grid = [["   " if x % 2 == 1 else "  "
                 for x in range((self.maze.width * 2) + 1)]
                for _ in range((self.maze.height * 2) + 1)]
        WALL_COLORS = [
                    "\033[107m",  # Index 0 : Blanc (Défaut)
                    "\033[48;5;130m",  # Index 1 : Rouge clair
                    "\033[102m",  # Index 2 : Vert clair
                    "\033[103m",  # Index 3 : Jaune clair
                    "\033[104m",  # Index 4 : Bleu clair
                    "\033[105m",  # Index 5 : Violet clair
                    "\033[106m"   # Index 6 : Cyan clair
                    ]
        final_path = self._get_path_cells()
        if self.maze.width > 8 and self.maze.height > 7:
            pat_42 = self.maze.pattern_42()
            self.color_42(grid, pat_42)

        for c in self.maze.grid:
            for i in range(0, self.maze.width):
                cx = (c[i].get_coord('x') * 2) + 1
                cy = (c[i].get_coord('y') * 2) + 1

                if c[i].get_direction("north") == 1:
                    grid[cy - 1][cx] = f'{WALL_COLORS[index]}   \033[0m'
                if c[i].get_direction("south") == 1:
                    grid[cy + 1][cx] = f'{WALL_COLORS[index]}   \033[0m'
                if c[i].get_direction("east") == 1:
                    grid[cy][cx + 1] = f'{WALL_COLORS[index]}  \033[0m'
                if c[i].get_direction("west") == 1:
                    grid[cy][cx - 1] = f'{WALL_COLORS[index]}  \033[0m'

                if (c[i].get_coord('x') == self.maze.entry['x']
                   and c[i].get_coord('y') == self.maze.entry['y']):
                    grid[cy][cx] = f"{"\033[41m"}   {"\033[0m"}"
                elif (c[i].get_coord('x') == self.maze.exit['x']
                      and c[i].get_coord('y') == self.maze.exit['y']):
                    grid[cy][cx] = f"{"\033[45m"}   {"\033[0m"}"

        if show_path is True:
            for k in range(len(final_path) - 1):
                cell_A = final_path[k]
                cell_B = final_path[k + 1]

                cx_A = (cell_A.get_coord('x') * 2) + 1
                cy_A = (cell_A.get_coord('y') * 2) + 1
                cx_B = (cell_B.get_coord('x') * 2) + 1
                cy_B = (cell_B.get_coord('y') * 2) + 1

                if not (cell_A.get_coord('x') == self.maze.entry['x']
                        and cell_A.get_coord('y') == self.maze.entry['y'] and
                        (not (cell_B.get_coord('x') == self.maze.exit['x'] and
                              cell_B.get_coord('y') == self.maze.exit['y']))):
                    grid[cy_A][cx_A] = "\033[44m   \033[0m"

                pont_x = (cx_A + cx_B) // 2
                pont_y = (cy_A + cy_B) // 2

                if pont_x % 2 == 1:
                    grid[pont_y][pont_x] = "\033[44m   \033[0m"
                else:
                    grid[pont_y][pont_x] = "\033[44m  \033[0m"

        for y in range(len(grid)):
            for x in range((self.maze.width * 2) + 1):
                if x % 2 == 0 and y % 2 == 0:
                    grid[y][x] = f"{WALL_COLORS[index]}  \033[0m"

        for row in grid:
            print("".join(row))

    def export(self, show_path: bool, index: int) -> None:
        WALL_COLORS = [
            "#FFFFFF",  # Index 0 : White (Default)
            "#D75F00",  # Index 1 : Dark orange / Rust (Matches \033[48;5;130m)
            "#90EE90",  # Index 2 : Light green
            "#FFFF99",  # Index 3 : Light yellow
            "#ADD8E6",  # Index 4 : Light blue
            "#DDA0DD",  # Index 5 : Light purple
            "#E0FFFF"   # Index 6 : Light cyan
            ]
        final_path = self._get_path_cells()

        cell_size = 10
        line = ''
        line += (f'<svg width="{(self.maze.width * 2 + 1) * cell_size}" '
                 f'height="{(self.maze.height * 2 + 1) * cell_size}" '
                 f'xmlns="http://www.w3.org/2000/svg">')
        line += (f'<rect x="0" y="0" '
                 f'width="{(self.maze.width * 2 + 1) * cell_size}" '
                 f'height="{(self.maze.height * 2 + 1) * cell_size}" '
                 f'fill="#000000" />')

        for c in self.maze.grid:
            for i in range(0, self.maze.width):
                cx = (c[i].get_coord('x') * 2) + 1
                cy = (c[i].get_coord('y') * 2) + 1

                if c[i].get_direction("north") == 1:
                    line += (f'<rect x="{cx * cell_size}" '
                             f'y="{(cy - 1) * cell_size}" '
                             f'width="10" height="10" '
                             f'fill="{WALL_COLORS[index]}" />')
                if c[i].get_direction("south") == 1:
                    line += (f'<rect x="{cx * cell_size}" '
                             f'y="{(cy + 1) * cell_size}" '
                             f'width="10" height="10" '
                             f'fill="{WALL_COLORS[index]}" />')
                if c[i].get_direction("east") == 1:
                    line += (f'<rect x="{(cx + 1) * cell_size}" '
                             f'y="{(cy) * cell_size}" '
                             f'width="10" height="10" '
                             f'fill="{WALL_COLORS[index]}" />')
                if c[i].get_direction("west") == 1:
                    line += (f'<rect x="{(cx - 1) * cell_size}" '
                             f'y="{(cy) * cell_size}" '
                             f'width="10" height="10" '
                             f'fill="{WALL_COLORS[index]}" />')

                if (c[i].get_coord('x') == self.maze.entry['x']
                   and c[i].get_coord('y') == self.maze.entry['y']):
                    line += (f'<rect x="{(cx) * cell_size}" '
                             f'y="{(cy) * cell_size}" '
                             f'width="10" height="10" fill="#FF0000" />')
                elif (c[i].get_coord('x') == self.maze.exit['x']
                      and c[i].get_coord('y') == self.maze.exit['y']):
                    line += (f'<rect x="{(cx) * cell_size}" '
                             f'y="{(cy) * cell_size}" '
                             f'width="10" height="10" fill="#663399" />')

        if show_path is True:
            for k in range(len(final_path) - 1):
                cell_A = final_path[k]
                cell_B = final_path[k + 1]

                cx_A = (cell_A.get_coord('x') * 2) + 1
                cy_A = (cell_A.get_coord('y') * 2) + 1
                cx_B = (cell_B.get_coord('x') * 2) + 1
                cy_B = (cell_B.get_coord('y') * 2) + 1

                if not (cell_A.get_coord('x') == self.maze.entry['x']
                        and cell_A.get_coord('y') == self.maze.entry['y'] and
                        (not (cell_B.get_coord('x') == self.maze.exit['x'] and
                              cell_B.get_coord('y') == self.maze.exit['y']))):
                    line += (f'<rect x="{(cx_A) * cell_size}" '
                             f'y="{(cy_A) * cell_size}" '
                             f'width="10" height="10" fill="#00BFFF" />')

                pont_x = (cx_A + cx_B) // 2
                pont_y = (cy_A + cy_B) // 2
                line += (f'<rect x="{(pont_x) * cell_size}" '
                         f'y="{(pont_y) * cell_size}" '
                         f'width="10" height="10" fill="#00BFFF" />')

        for y in range((self.maze.height * 2) + 1):
            for x in range((self.maze.width * 2) + 1):
                if x % 2 == 0 and y % 2 == 0:
                    line += (f'<rect x="{x * cell_size}" y="{(y) * cell_size}"'
                             f' width="10" height="10" '
                             f'fill="{WALL_COLORS[index]}" />')

        if self.maze.width > 8 and self.maze.height > 7:
            pat_42 = self.maze.pattern_42()
            for c in self.maze.grid:
                for i in range(0, self.maze.width):
                    cx = (c[i].get_coord('x') * 2) + 1
                    cy = (c[i].get_coord('y') * 2) + 1
                    if c[i] in pat_42:
                        line += (f'<rect x="{cx * cell_size}" '
                                 f'y="{(cy) * cell_size}" '
                                 f'width="10" height="10" fill="#808080" />')

        line += ('</svg>')
        with open("maze.svg", 'w') as file:
            file.write(line)
