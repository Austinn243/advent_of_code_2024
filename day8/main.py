"""
Advent of Code 2024, Day 8
Resonant Collinearity
https://adventofcode.com/2024/day/8
"""

from collections import defaultdict
from itertools import combinations
from os import path
from typing import Callable, NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"
NO_ANTENNA = "."

AntennaMap = list[str]
Frequency = str


class Position(NamedTuple):
    """A position in the antenna map."""

    x: int
    y: int


def read_antenna_map(filename: str) -> AntennaMap:
    """Read the antenna map from the specified file and return it as a list of lists."""

    with open(filename) as file:
        return [line.strip() for line in file]


def count_distinct_antinodes(
    antenna_map: AntennaMap,
    find_antinodes: Callable[[AntennaMap, Position, Position], list[Position]],
) -> int:
    """Count the number of distinct antinodes in the antenna map."""

    antenna_positions_by_frequency = find_antennae(antenna_map)

    distinct_antinode_positions = set()

    for antenna_positions in antenna_positions_by_frequency.values():
        for antenna_position_pair in combinations(antenna_positions, 2):
            antinode_positions = find_antinodes(antenna_map, *antenna_position_pair)
            distinct_antinode_positions.update(antinode_positions)

    return len(distinct_antinode_positions)


def find_antennae(antenna_map: AntennaMap) -> dict[Frequency, set[Position]]:
    """Find the positions of all the antennae in the antenna map.

    The located antennae are grouped together by the frequency they emit.
    """

    antenna_positions: dict[Frequency, set[Position]] = defaultdict(set)

    for y, row in enumerate(antenna_map):
        for x, frequency in enumerate(row):
            if frequency == NO_ANTENNA:
                continue

            position = Position(x, y)
            antenna_positions[frequency].add(position)

    return antenna_positions


def find_antinode_pair(
    antenna_map: AntennaMap,
    antenna1_position: Position,
    antenna2_position: Position,
) -> list[Position]:
    """Find the positions of the two antinodes for the specified antennae.

    These antinodes are the same distance from their respective antennae as the antennae
    are from each other.
    """

    x_diff = antenna2_position.x - antenna1_position.x
    y_diff = antenna2_position.y - antenna1_position.y

    antinode1_x = antenna1_position.x - x_diff
    antinode1_y = antenna1_position.y - y_diff
    antinode1 = Position(antinode1_x, antinode1_y)

    antinode2_x = antenna2_position.x + x_diff
    antinode2_y = antenna2_position.y + y_diff
    antinode2 = Position(antinode2_x, antinode2_y)

    return [
        antinode
        for antinode in [antinode1, antinode2]
        if is_within_bounds(antinode, antenna_map)
    ]


def find_all_antinodes(
    antenna_map: AntennaMap,
    antenna1_position: Position,
    antenna2_position: Position,
) -> list[Position]:
    """Find the positions of all antinodes for the specified antennae.

    The antennae and their antinodes are the same distance apart.
    """

    x_diff = antenna2_position.x - antenna1_position.x
    y_diff = antenna2_position.y - antenna1_position.y

    antinode_positions = []
    antinode_position = antenna1_position

    while is_within_bounds(antinode_position, antenna_map):
        antinode_positions.append(antinode_position)

        antinode_position = Position(
            antinode_position.x + x_diff, antinode_position.y + y_diff
        )

    antinode_position = antenna2_position

    while is_within_bounds(antinode_position, antenna_map):
        antinode_positions.append(antinode_position)

        antinode_position = Position(
            antinode_position.x - x_diff, antinode_position.y - y_diff
        )

    return antinode_positions


def is_within_bounds(position: Position, antenna_map: AntennaMap) -> bool:
    """Determine if the specified position is within the bounds of the antenna map."""

    x, y = position
    return 0 <= x < len(antenna_map[0]) and 0 <= y < len(antenna_map)


def main() -> None:
    """Read the antenna map from the input file and process it."""

    input_file = INPUT_FILE

    file_path = path.join(path.dirname(__file__), input_file)

    antenna_map = read_antenna_map(file_path)
    print(antenna_map)

    print(count_distinct_antinodes(antenna_map, find_antinode_pair))
    print(count_distinct_antinodes(antenna_map, find_all_antinodes))


if __name__ == "__main__":
    main()
