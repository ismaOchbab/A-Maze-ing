# import os
# from maze import Maze
# from maze_generator import MazeGenerator
# from visualizer import MazeRenderer
# import sys
# from parser import Parsing, ConfigError


# def main() -> None:
#     # Initialisation séparée
#     if len(sys.argv) != 2:
#         print("Usage: python3 parser.py config.txt")
#         sys.exit(1)

#     parser = Parsing(sys.argv[1])
#     try:
#         parser.parse()
#     except ConfigError as e:
#         print(f"Configuration error: {e}")
#         sys.exit(1)

#     maze = Maze(parser.width, parser.height,
#                 parser.output_file, parser.entry,
#                 parser.exit)
#     generator = MazeGenerator(maze, parser.seed)
#     renderer = MazeRenderer(maze)
#     generator.generate(parser.perfect, renderer, 0)

#     show_path = True
#     i = 0
#     rend = True

#     while True:
#         os.system('clear')
#         renderer.display(show_path, i)
#         maze.hexa_output()

#         choice = input("\n=== A-Maze-ing ===\n1. Re-generate a new maze\n2. "
#                        "Show/Hide path from entry to exit\n3. "
#                        "Rotate maze colors\n4. "
#                        "Export maze in .svg\n5. "
#                        "Show/Hide maze animation\n6. "
#                        "Quit\nChoice? (1-6): ")
#         if choice == '1':
#             # On recrée les objets pour relancer une génération fraîche
#             maze = Maze(parser.width, parser.height, parser.output_file,
#                         parser.entry, parser.exit)
#             generator = MazeGenerator(maze, parser.seed)
#             renderer = MazeRenderer(maze)
#             if rend is True:
#                 generator.generate(parser.perfect, renderer, i)
#             else:
#                 generator.generate(parser.perfect)
#         if choice == '2':
#             if show_path is True:
#                 show_path = False
#             else:
#                 show_path = True
#         if choice == '3':
#             i += 1
#             if i > 6:
#                 i = 0
#         if choice == '4':
#             renderer.export(show_path, i)
#         if choice == '5':
#             if rend:
#                 rend = False
#             else:
#                 rend = True
#         if choice == '6':
#             break


# if __name__ == "__main__":
#     main()
