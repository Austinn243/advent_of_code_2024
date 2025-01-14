"""
Advent of Code 2024, Day 20
Race Condition
https://adventofcode.com/2024/day/20
"""

from enum import Enum
from functools import partial
from os import path
from typing import NamedTuple, Optional

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

CHEAT_DISTANCE = 2
MEANINGFUL_CHEAT_COST = 100


class Cell(Enum):
    """Represents a cell in the racetrack."""

    EMPTY = "."
    WALL = "#"
    START = "S"
    FINISH = "E"


class Position(NamedTuple):
    """A position in the racetrack."""

    x: int
    y: int


Racetrack = list[Cell]


def interpret_char_as_cell(char: str) -> Cell:
    """Interpret a character as a cell in the racetrack."""

    return Cell(char)


def read_racetrack(file_path: str) -> Racetrack:
    """Read the racetrack layout from a file."""

    racetrack = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            racetrack.append([interpret_char_as_cell(char) for char in line.strip()])

    return racetrack


def print_racetrack(racetrack: Racetrack) -> None:
    """Print the racetrack layout."""

    for row in racetrack:
        print("".join(cell.value for cell in row))


def find_start_position(racetrack: Racetrack) -> Position:
    """Find the starting position in the racetrack."""

    for y, row in enumerate(racetrack):
        for x, cell in enumerate(row):
            if cell == Cell.START:
                return Position(x, y)

    raise ValueError("No starting position found in the racetrack.")


def is_within_bounds(position: Position, racetrack: Racetrack) -> bool:
    """Check if a position is within the bounds of the racetrack."""

    return 0 <= position.y < len(racetrack) and 0 <= position.x < len(racetrack[0])


def find_neighbors(
    position: Position,
    racetrack: Racetrack,
    offset: int,
) -> list[Position]:
    """Find the neighbors of a position."""

    all_neighbors = [
        Position(position.x - offset, position.y),
        Position(position.x + offset, position.y),
        Position(position.x, position.y - offset),
        Position(position.x, position.y + offset),
    ]

    return [
        neighbor
        for neighbor in all_neighbors
        if is_within_bounds(neighbor, racetrack)
        and racetrack[neighbor.y][neighbor.x] != Cell.WALL
    ]


find_direct_neighbors = partial(find_neighbors, offset=1)
find_cheat_neighbors = partial(find_neighbors, offset=CHEAT_DISTANCE)


def find_next_node(
    position: Position,
    racetrack: Racetrack,
    visited: set[Position],
) -> Optional[Position]:
    """Find the next node to visit in the racetrack."""

    neighbors = find_direct_neighbors(position, racetrack)

    for neighbor in neighbors:
        if neighbor not in visited:
            return neighbor

    return None


def evaluate_path_costs(
    racetrack: Racetrack,
    start_position: Optional[Position] = None,
) -> dict[Position, int]:
    """Evaluate the path through the racetrack."""

    path_nodes = {}

    current_position = start_position or find_start_position(racetrack)
    current_cost = 0
    visited = set()

    while current_position:
        path_nodes[current_position] = current_cost
        visited.add(current_position)

        current_position = find_next_node(current_position, racetrack, visited)
        current_cost += 1

    return path_nodes


def count_meaningful_cheats(
    racetrack: Racetrack,
    path_node_costs: dict[Position, int],
    meaningful_cheat_cost: int = MEANINGFUL_CHEAT_COST,
) -> int:
    """Count the number of meaningful cheats in the racetrack."""

    meaningful_cheat_count = 0

    for position, cost in path_node_costs.items():
        cheat_neighbors = find_cheat_neighbors(position, racetrack)
        neighbor_costs = [path_node_costs[neighbor] for neighbor in cheat_neighbors]

        for neighbor_cost in neighbor_costs:
            # NOTE: We remove 1 from the neighbor cost to account for the
            # standard cost of moving between nodes. We're measuring how much
            # time we can save by cheating, not the cost of cheating itself.
            if neighbor_cost - cost - 1 >= meaningful_cheat_cost:
                meaningful_cheat_count += 1

    return meaningful_cheat_count


def main() -> None:
    """Read the racetrack layout from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    racetrack = read_racetrack(file_path)
    print_racetrack(racetrack)

    path_node_costs = evaluate_path_costs(racetrack)
    print(path_node_costs)

    meaningful_cheat_count = count_meaningful_cheats(racetrack, path_node_costs)
    print(meaningful_cheat_count)


if __name__ == "__main__":
    main()
