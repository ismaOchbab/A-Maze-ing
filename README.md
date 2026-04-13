*This project has been created as part of the 42 curriculum by ichbab & ykouiri*

# A_maze_ing

## Description

The goal of the project is to create and visualize a maze, randomly generated, with a 42 pattern inside of it. Given a config file with an entry and an exit coordinates, we also have to provide a path-finding algorithm that solves the shortest path from entry to exit. This result will be written in an output given file, in an hexadecimal wall representation of each cell.
The code is organized so that the generation logic can be used later (PACMAN project)

## Resolution breakdown

### Configuration file parsing

On this project, we first need to parse informations from a configuration file. This implies ignoring comments and invalid flags.

|Type|Flag|Expected value|Format|Description|
|---|---|---|---|---|
|Mandatory|WIDTH|int >= 0|WIDTH=20|Maze width
|Mandatory|HEIGHT|int >= 0|HEIGHT=20|Maze height
|Mandatory|ENTRY|x & y within available dimensions|ENTRY=1,2|Entry point for path-finding
|Mandatory|EXIT|x & y within available dimensions|EXIT=4,6|Exit point for path-finding
|Mandatory|OUTPUT_FILE|string|OUTPUT_FILE=maze.txt|Output file path
|Mandatory|PERFECT|bool|PERFECT=True|If the maze has one path or more
|Extra|SEED|string|SEED=1|Generation seed
|Extra|DISPLAY_FT_PATTERN|bool|DISPLAY_FT_PATTERN=False|Add/remove the 42 logo in the center
|Extra|ANIMATION|bool|ANIMATION=True|Animate the maze generation
|Extra|SHOW_PATH|bool|SHOW_PATH=True|Displays the shortest path when the maze is generated

Example of a valid configuration file :
```
# Dimensions
WIDTH=9
HEIGHT=8

# Entry/Exit coordinates
ENTRY=0,0
EXIT=7,7

# Enable/disable perfect maze
PERFECT=true

# Maze output file path, should not contain spaces
OUTPUT_FILE=maze.txt

# Seed-based generation
SEED=1

# Show/Hide the shortest path
SHOW_PATH=true

# Show the 42 patern. Default in center if entry/exit coords make it possible
DISPLAY_FT_PATTERN=True
```

### Maze generation

Next step is the generation of a maze following the requirements in the config file. While it is not asked in the subject, we included a generation animation as a bonus in the project.

### Maze animation

We decided to use the terminal to visualize our maze :



### Generation algorithm

We used the recursive backtracker algorithm to generate the maze: A stack is created where each visited cell is added to the stack. The algorythm starts at the entry point, and visit a random neighbouring cell (based on the seed) that is breakable (ignoring the protected cells like the 42 logo cells, and the maze's border cells). The previous cell is added to the stack, and the program continues to select a random neighbouring cell until it reaches a dead end. In this case, it goes back in the stack, cell by cell, until it finds one with a neighbouring cell that he hasn't visited yet. This process will automatically create a perfect maze, so we have to break random walls to make it imperfect. [For a better understanding click here](https://www.jamisbuck.org/presentations/rubyconf2011/index.html#recursive-backtracker). 

We chose this algorithm because it's easy to understand and well known.

### Path-Finding algorithm

We used a simple "propagation" algorithm. Starting from the entry, all neighbouring cells become "active cells" and check their own neighbouring cells, repeating this process until the exit is found. The propagation history of the final cell is then the shortest path.

### Interactive control keys

During the execution of our project, it is possible to interact with it with the following keys:

|Key|Interaction|
|---|---|
|c|Change color|
|r|Regenerate the maze|
|Enter ↩|Resume animation|


### Result output

The resut maze, its entry/exit coordinates and its shortest path are saved in the given output file (OUTPUT_FILE flag in the config.txt) in the following format :

- Hexadecimal representation of the cells where each digit encodes which walls are closed, following this principle:

    |Bit|Direction|
    |---|---|
    |0 (LSB)|North|
    |1|East|
    |2|South|
    |3|West|
        A closed wall is a bit to 1, so 1010 means that east and west are closed.

- Entry coords: (x,y)
- Exit coords: (x,y)
- The shortest path to solve the maze, with each move corresponding to a direction to go to (N=north, E=east, ...)

### Python package creation

The second goal of the a-maze-ing project is to create a Python package from our work, reusable in a future project. This python package will make us enable to generate a Maze using the MazeGenerator object.

## Instructions

You will need to have Make, UV and python installed on your pc.

To install the venv and dependencies, use:
```bash
make install
```

To run the program, use : 
```bash
uv run python a_maze_ing.py <configuration_file_path>
```
or
```bash
make run
```

#### Make commands
|Utility|Command|
|---|---|
|Installation|```make install```|
|Running program|```make run```|
|Check norm|```make lint-strict```|
|Remove uselss files|```make clean```|
|Remove uselss files and reinstall|```make re```|
|Build package|```make build```|
|Debug (CLI)|```make debug```|

## Resources

#### Useful links
- [Maze generation algorithm](https://www.jamisbuck.org/presentations/rubyconf2011/index.html#recursive-backtracker-demo)
- [Flushing stdin](http://jamescherti.com/python-flushing-stdin-before-using-input-function/)
- [Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm/)

## Additional informations

#### Reusable code
We made the program so that the MazeGenerator is reusable in another project. The user can add this object in its code by installing the package generated with the ```make build``` comand. It can then be used with this simple example:
```python

from mazegen import Cell, MazeGenerator, Maze, Parsing

def main():

    # Setup a configuration variable
    config = Config(width=8,
                    height=8,
                    entry_coords={'x': 0, 'y': 0},
                    exit_coords={'x': 7, 'y': 7},
                    output_file='test.txt',
                    perfect=False,
                    seed='laurent',
                    animation=True,
                    show_path=True,
                    display_ft_pattern=True)

    # Create a maze
    generator = MazeGenerator(config)
    generator.create_maze()

    # Generate the maze's content
    list(generator.generate_existing_maze())

    # Dig holes to make it unperfect
    generator.maze.make_maze_perfect(True)

    # Generate the shortest path
    PathFinder.find_path(generator.maze)

    # Save the maze to a file
    generator.maze.output_maze(config.output_file)

if __name__ == "__main__":
    main()

```


#### AI usage
In the realisation of this project, AI was used in various tasks, but mostly troubleshooting and research :

- Fixing strange error codes
- Various questions about how to use different modules
- Understanding how algorithms work and how to implement them

#### Planification



We will take this in consideration for the future projects: ***<ins>Planning is not an option</ins>***.

#### Specific tools used

|Tool|Usage|
|---|---|
|argparse (python package)|Argument parsing|
|pynput (python package)|Keyboard keys interception|
|pydantic (python package)|Data validation for parsing|
|flake8 (python package)|Check the flake8 norm|
|mypy (python package)|Check the mypy norm|
|uv (python package manager)|Project management and package building|

## Authors and contributions

[]

- Configuration, Cell and Maze objects
- Pathfinding and generation algorithm
- Package build
- Readme

[]

- Controller object (Maze interruption)
- MazeVisualizer object to visualize the maze
- Colors, Reset, Pause interactions

