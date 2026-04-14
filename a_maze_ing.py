#!/usr/bin/env python3

import os
import sys
from mazegen.maze import Maze
from mazegen.maze_generator import MazeGenerator
from mazegen.visualizer import MazeRenderer
from mazegen.parser import Parsing, ConfigError
from mazegen_bonus.maze import Maze as Maze2
from mazegen_bonus.maze_generator import MazeGenerator as MazeGenerator2
from mazegen_bonus.visualizer import MazeRenderer as MazeRenderer2
from mazegen_bonus.parser import Parsing as Parsing2


def ask_choice() -> int:
    while True:
        choice = input(
            "Make your choice:\n"
            "1- Main Generator\n"
            "2- Bonus Generator\n"
            "3- Quit this menu\n"
        ).strip()

        if choice in ('1', '2', '3'):
            return int(choice)

        print("Invalid choice. Enter 1 or 2 or 3")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    answer = ask_choice()
    if answer == 1:
        parser = Parsing(sys.argv[1])
        try:
            parser.parse()
        except ConfigError as e:
            print(f"Configuration error: {e}")
            sys.exit(1)

        maze = Maze(parser.width,
                    parser.height,
                    parser.output_file,
                    parser.entry,
                    parser.exit)
        generator = MazeGenerator(maze, parser.seed)
        renderer = MazeRenderer(maze)
        generator.generate(parser.perfect, renderer, 0)

        show_path = True
        i = 0
        rend = True

        while True:
            os.system('clear')
            renderer.display(show_path, i)
            maze.hexa_output()
            if maze.width <= 8 or maze.height <= 7:
                print("\nWarning: Maze too small to render the '42' pattern\n")

            choice = input("""\n=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Export maze in .svg
5. Show/Hide maze animation
6. Quit
Choice? (1-6): """)
            if choice == '1':
                # On recrée les objets pour relancer une génération fraîche
                maze = Maze(parser.width, parser.height, parser.output_file,
                            parser.entry, parser.exit)
                generator = MazeGenerator(maze, parser.seed)
                renderer = MazeRenderer(maze)
                if rend is True:
                    generator.generate(parser.perfect, renderer, i)
                else:
                    generator.generate(parser.perfect)
            if choice == '2':
                if show_path is True:
                    show_path = False
                else:
                    show_path = True
            if choice == '3':
                i += 1
                if i > 6:
                    i = 0
            if choice == '4':
                renderer.export(show_path, i)
            if choice == '5':
                if rend:
                    rend = False
                else:
                    rend = True
            if choice == '6':
                break
    elif answer == 2:
        try:
            parser2 = Parsing2(sys.argv[1])
            parser2.parse()
            maze2 = Maze2(parser2)
            maze2.apply_42_pattern()

            generator2 = MazeGenerator2(maze2)
            generator2.generate()

            renderer2 = MazeRenderer2(generator2.maze, generator2, parser2)
            renderer2.run()
        except Exception as e:
            print(
                f"Caught an error: {e}"
            )
            exit()
    else:
        print("Exiting..")
        exit()
    return None


if __name__ == "__main__":
    # sys.exit(main())
    main()
