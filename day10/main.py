"""
Advent of Code, Day 10
Hoof It
https://adventofcode.com/2024/day/10
"""

from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

TRAIL_START = 0
TRAIL_END = 9


Height = int
AreaMap = list[list[Height]]


class Position(NamedTuple):
    """A position on the area map."""

    x: int
    y: int


def read_area_map(file_path: str) -> AreaMap:
    """Read an area map from the input file."""

    rows = []
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            rows.append(row)

    return rows


def is_within_bounds(position: Position, area_map: AreaMap) -> bool:
    """Check if a position is within the bounds of the area map."""

    x, y = position
    return 0 <= x < len(area_map[0]) and 0 <= y < len(area_map)


def trailhead_positions(area_map: AreaMap) -> list[Position]:
    """Find the positions of all trailheads on the area map."""

    trailhead_positions = []
    for y, row in enumerate(area_map):
        for x, cell in enumerate(row):
            if cell == TRAIL_START:
                trailhead_positions.append(Position(x, y))

    return trailhead_positions


def new_neighbors(
    position: Position,
    area_map: AreaMap,
    visited: set[Position],
) -> list[Position]:
    possible_neighbors = [
        Position(position.x - 1, position.y),
        Position(position.x + 1, position.y),
        Position(position.x, position.y - 1),
        Position(position.x, position.y + 1),
    ]

    return [
        neighbor
        for neighbor in possible_neighbors
        if is_within_bounds(neighbor, area_map)
        and neighbor not in visited
        and (area_map[neighbor.y][neighbor.x] - area_map[position.y][position.x] == 1)
    ]


def trailhead_score(area_map: AreaMap, trailhead_position: Position) -> int:
    """Calculate the trailhead score for a trailhead on the area map.

    The score of a trailhead is the number of full trails that stem from it.
    """

    trail_end_positions = set()

    def visit(position: Position, visited: set[Position]) -> None:
        nonlocal trail_end_positions

        height = area_map[position.y][position.x]
        if height == TRAIL_END:
            trail_end_positions.add(position)
            return

        visited.add(position)

        for neighbor in new_neighbors(position, area_map, visited):
            visit(neighbor, visited)

    visit(trailhead_position, set())
    return len(trail_end_positions)


def trailhead_rating(area_map: AreaMap, trailhead_position: Position) -> int:
    """Calculate the trailhead rating for a trailhead on the area map.

    The rating of a trailhead is the number of distinct trails that stem from it.
    """

    trail_end_count = 0

    def visit(position: Position, visited: set[Position]) -> None:
        nonlocal trail_end_count

        height = area_map[position.y][position.x]
        if height == TRAIL_END:
            trail_end_count += 1
            return

        visited.add(position)

        for neighbor in new_neighbors(position, area_map, visited):
            visit(neighbor, visited.copy())

    visit(trailhead_position, set())
    return trail_end_count


def main() -> None:
    """Read an area map from an input file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    area_map = read_area_map(file_path)
    print(area_map)

    trailheads = trailhead_positions(area_map)
    print(trailheads)

    scores = [trailhead_score(area_map, trailhead) for trailhead in trailheads]
    print(scores)
    print(sum(scores))

    ratings = [trailhead_rating(area_map, trailhead) for trailhead in trailheads]
    print(ratings)
    print(sum(ratings))


if __name__ == "__main__":
    main()
