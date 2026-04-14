#!/usr/bin/env python3

"""Main entry point for the A-Maze-ing project."""

import sys
from parser import Parsing, ConfigError
from maze import Maze
from maze_generator import MazeGenerator
from visualizer import MazeRenderer


class MazeError(Exception):
    """Raised when maze generation or validation fails."""


def build_maze(config_path: str) -> tuple[Maze, Parsing]:
    """Build and generate a maze from a configuration file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        A tuple containing the generated Maze instance and the parsed config.

    Raises:
        ConfigError: If the configuration file is invalid.
        MazeError: If the generated maze does not satisfy the subject rules.
    """
    parser = Parsing(config_path)
    parser.parse()

    maze = Maze(parser)

    pattern_applied = maze.apply_42_pattern()
    if not pattern_applied:
        print(
            "Warning: maze too small to place the '42' pattern.",
            file=sys.stderr
            )

    generator = MazeGenerator(maze)
    generator.generate()

    if not maze.validate():
        raise MazeError("Generated maze is invalid")

    return maze, parser


def write_output_file(maze: Maze, output_path: str) -> None:
    """Write the generated maze to the required output file.

    Args:
        maze: The generated maze.
        output_path: Destination file path.

    Raises:
        MazeError: If the file cannot be written.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(maze.to_hex_output())
    except OSError as exc:
        raise MazeError(
            f"Cannot write output file '{output_path}': {exc}") from exc


def run(config_path: str) -> Maze:
    """Execute the full maze workflow.

    Args:
        config_path: Path to the configuration file.

    Returns:
        The generated and validated maze.

    Raises:
        ConfigError: If the configuration file is invalid.
        MazeError: If generation, validation, or file writing fails.
    """
    maze, parser = build_maze(config_path)
    write_output_file(maze, parser.output_file)
    return maze


def main() -> int:
    """Program entry point.

    Returns:
        Process exit code.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        run(sys.argv[1])
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except MazeError as exc:
        print(f"Maze error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    # sys.exit(main())
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        exit()

    try:
        parser = Parsing(sys.argv[1])
        parser.parse()
        maze = Maze(parser)
        maze.apply_42_pattern()

        generator = MazeGenerator(maze)
        generator.generate()

        write_output_file(maze, parser.output_file)

        renderer = MazeRenderer(generator.maze, generator, parser)
        renderer.run()
    except Exception as e:
        print(
            f"Caught an error: {e}"
        )
        exit()
