"""
Advent of Code 2024, Day 15
Warehouse Woes
https://adventofcode.com/2024/day/15
"""

from enum import Enum
from os import path
from pprint import pprint
from typing import Callable, NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"


GPS_COORDINATE_Y_MULTIPLIER = 100


class Position(NamedTuple):
    """Represents a position relative to the top-left corner of the warehouse."""

    x: int
    y: int


class Cell(Enum):
    """Represents the entity at a position in the warehouse."""

    BOX = "O"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    EMPTY = "."
    ROBOT = "@"
    WALL = "#"

    def __str__(self) -> str:
        """Convert the cell to a user-friendly string representation."""

        return self.value


class Move(Enum):
    """Represents a direction of movement that the robot can take."""

    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def __repr__(self) -> str:
        """Convert the move to a string representation for debugging."""

        return self.name.capitalize()

    def apply(self, position: Position) -> Position:
        """Apply the move to a position and return the new position."""

        return Position(position.x + self.value[0], position.y + self.value[1])


Grid = list[list[Cell]]


def read_inputs(
    file_path: str,
) -> tuple[list[list[str]], list[str]]:
    """Read the raw warehouse layout and moves from a file."""

    lines = None

    with open(file_path, encoding="utf-8") as file:
        lines = iter(file.readlines())

    warehouse = []

    while (line := next(lines).strip()) != "":
        warehouse.append(list(line))

    moves = [char for line in lines for char in line.strip()]

    return warehouse, moves


def interpret_warehouse_layout(
    raw_layout: list[list[str]],
    interpret_char: Callable[[str], list[Cell]],
) -> Grid:
    """Interpret the raw warehouse layout as a grid of cells."""

    warehouse = []

    for row in raw_layout:
        warehouse_row = []

        for char in row:
            warehouse_row.extend(interpret_char(char))

        warehouse.append(warehouse_row)

    return warehouse


def interpret_char_as_single_cells(char: str) -> list[Cell]:
    """Interpret a character as a single cell in the warehouse."""

    match char:
        case "O":
            return [Cell.BOX]
        case ".":
            return [Cell.EMPTY]
        case "@":
            return [Cell.ROBOT]
        case "#":
            return [Cell.WALL]
        case _:
            raise ValueError(f"Invalid cell: {char}")


def interpret_char_as_upscaled_cells(char: str) -> list[Cell]:
    """Interpret a character as two cells in the warehouse after upscaling."""

    match char:
        case "O":
            return [Cell.BOX_LEFT, Cell.BOX_RIGHT]
        case ".":
            return [Cell.EMPTY, Cell.EMPTY]
        case "@":
            return [Cell.ROBOT, Cell.EMPTY]
        case "#":
            return [Cell.WALL, Cell.WALL]
        case _:
            raise ValueError(f"Invalid cell: {char}")


def interpret_char_as_move(char: str) -> Move:
    """Interpret a character as a move in the warehouse."""

    match char:
        case "^":
            return Move.NORTH
        case "v":
            return Move.SOUTH
        case ">":
            return Move.EAST
        case "<":
            return Move.WEST
        case _:
            raise ValueError(f"Invalid move: {char}")


def find_empty_position(
    warehouse: Grid,
    starting_position: Position,
    move: Move,
) -> Position:
    """Find the first empty position in the direction of the move after a box."""

    position = starting_position

    while True:
        position = move.apply(position)
        cell = warehouse[position.y][position.x]

        if cell == Cell.EMPTY:
            return position

        if cell == Cell.WALL:
            return None


def swap(warehouse: Grid, position1: Position, position2: Position) -> None:
    """Swap the entities at two positions in the warehouse."""

    warehouse[position1.y][position1.x], warehouse[position2.y][position2.x] = (
        warehouse[position2.y][position2.x],
        warehouse[position1.y][position1.x],
    )


def push_entities(
    warehouse: Grid,
    source_position: Position,
    target_position: Position,
    move: Move,
) -> Position:
    pass


# NOTE: The robot is not the only entity that can move boxes; the boxes themselves
# can also move other boxes. This means that we could define our pushing function
# as a recursive function that operates on entities that move and push other entities.
# This might be a more flexible option than defining separate functions specifically
# based around the robot itself. It might also remove some duplicated logic. However
# it may also be less performant than our old small box pushing function, which
# was able to skip moving every box in the line of boxes because it knew that the
# only entities being moved were in the same line, whereas our extended use cases
# also include big boxes that span multiple lines and can move boxes in those lines.
# Optionally, we could also just define this function around big boxes since our
# example won't be expanded beyond this point.


def push_small_box(
    warehouse: Grid,
    robot_position: Position,
    box_position: Position,
    move: Move,
) -> Position:
    """Push a small box and return the robot's new position.

    Any other small boxes in the way will also be pushed in the same direction.
    """

    next_empty_position = find_empty_position(
        warehouse,
        box_position,
        move,
    )

    if not next_empty_position:
        return robot_position

    swap(warehouse, box_position, next_empty_position)
    swap(warehouse, robot_position, box_position)
    return box_position


def push_large_box(
    warehouse: Grid,
    robot_position: Position,
    box_position: Position,
    move: Move,
) -> Position:
    """Push a large box and return the robot's new position.

    Any other large boxes in the way will also be pushed in the same direction.
    This also includes boxes that are only partially in the way.
    """

    # TODO

    return robot_position


def simulate_robot_movements(warehouse: Grid, moves: list[Move]) -> Grid:
    """Simulate the robot's movements in the warehouse and return the final layout."""

    new_layout = [row.copy() for row in warehouse]
    robot_position = find_robot_position(warehouse)

    for move in moves:
        next_position = move.apply(robot_position)
        cell = new_layout[next_position.y][next_position.x]

        match cell:
            case Cell.BOX:
                robot_position = push_small_box(
                    new_layout,
                    robot_position,
                    next_position,
                    move,
                )

            case Cell.BOX_LEFT | Cell.BOX_RIGHT:
                robot_position = push_large_box(
                    new_layout,
                    robot_position,
                    next_position,
                    move,
                )

            case Cell.EMPTY:
                swap(new_layout, robot_position, next_position)
                robot_position = next_position

            case _:
                continue

    return new_layout


def find_robot_position(warehouse: Grid) -> Position:
    """Find the position of the robot in the warehouse."""

    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell == Cell.ROBOT:
                return Position(x, y)

    raise ValueError("Robot not found in warehouse.")


def find_box_positions(warehouse: Grid) -> list[Position]:
    """Find the positions of all boxes in the warehouse."""

    box_positions = []

    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell == Cell.BOX:
                box_positions.append(Position(x, y))

    return box_positions


def gps_coordinate(box_position: Position) -> int:
    """Calculate the GPS coordinate of a box in the warehouse."""

    return box_position.y * GPS_COORDINATE_Y_MULTIPLIER + box_position.x


def print_warehouse(warehouse: Grid) -> None:
    """Print the warehouse layout to the console."""

    for row in warehouse:
        print("".join(str(cell) for cell in row))


def main() -> None:
    """Read information about the warehouse and the robot's movements and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    raw_warehouse_layout, raw_moves = read_inputs(file_path)

    moves = [interpret_char_as_move(char) for char in raw_moves]
    initial_warehouse_layout = interpret_warehouse_layout(
        raw_warehouse_layout,
        interpret_char_as_single_cells,
    )

    final_warehouse_layout = simulate_robot_movements(initial_warehouse_layout, moves)
    print_warehouse(final_warehouse_layout)

    box_positions = find_box_positions(final_warehouse_layout)

    gps_coordinates = [gps_coordinate(position) for position in box_positions]
    print(sum(gps_coordinates))

    upscaled_initial_warehouse_layout = interpret_warehouse_layout(
        raw_warehouse_layout,
        interpret_char_as_upscaled_cells,
    )
    print_warehouse(upscaled_initial_warehouse_layout)


if __name__ == "__main__":
    main()
