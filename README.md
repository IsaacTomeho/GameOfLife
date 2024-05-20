# Conway's Game of Life

This project implements Conway's Game of Life using Python and Pygame. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. The game consists of a grid of cells, each of which can be alive or dead. The state of the grid evolves over discrete time steps according to a set of simple rules.

## Features

- **Dynamic Grid Size**: The grid size adjusts according to the window size and the zoom level.
- **Random Initial State**: The grid is initialized with a random configuration of live and dead cells.
- **Zoom and Pan**: You can zoom in and out to see more or less detail of the grid and pan around the grid using the mouse.
- **Pause and Resume**: Pause and resume the simulation using keyboard shortcuts or the control panel.
- **Save and Load State**: Save the current state of the grid to a file and load it back later.
- **Customizable Speed**: Adjust the speed of the simulation using keyboard shortcuts.

## Controls

- **Space**: Pause/Resume the simulation.
- **R**: Reset the grid with a new random configuration.
- **S**: Save the current state of the grid.
- **L**: Load a previously saved state.
- **Arrow Up/Down**: Increase/Decrease the speed of the simulation.
- **+/-**: Zoom in/out.
- **Mouse Left Click**: Set a cell to alive.
- **Mouse Right Click**: Set a cell to dead.
- **Mouse Middle Button + Drag**: Pan the grid.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/game-of-life.git
    cd game-of-life
    ```

2. **Install the required dependencies**:
    ```bash
    pip install pygame numpy
    ```

3. **Run the game**:
    ```bash
    python game_of_life.py
    ```

## Requirements

- Python 3.x
- Pygame
- NumPy

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- John Horton Conway for creating the Game of Life.
- The Pygame and NumPy communities for their excellent libraries.
