"""
Advent of Code 2024, Day 6
Guard Gallivant
https://adventofcode.com/2024/day/6
"""

from collections.abc import Generator
from enum import Enum
from itertools import pairwise
from os import path
from typing import NamedTuple, Optional

INPUT_FILE = "input.txt"
EMPTY = "."


OBSTACLE = "#"
START = "^"


Map = list[str]


class Position(NamedTuple):
    """Represents a position on the map."""

    x: int
    y: int


class Direction(Enum):
    """Represents a direction the guard can travel."""

    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)

    def advance(self, position: Position) -> Position:
        """Advance the guard in the current direction."""

        dx, dy = self.value

        return Position(position.x + dx, position.y + dy)

    def rotate_clockwise(self) -> "Direction":
        """Rotate the direction 90 degrees clockwise."""

        if self is Direction.North:
            return Direction.East

        if self is Direction.East:
            return Direction.South

        if self is Direction.South:
            return Direction.West

        return Direction.North


class Step(NamedTuple):
    """Represents a step in the guard's patrol route."""

    position: Position
    direction: Direction


def read_map(file_path: str) -> Map:
    """Read the map from the specified file."""

    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


def find_start(area_map: Map) -> Position:
    """Locate the guard's starting position on the map."""

    for y, row in enumerate(area_map):
        for x, cell in enumerate(row):
            if cell == START:
                return Position(x, y)

    raise ValueError("No starting position found.")


def is_valid_position(area_map: Map, position: Position) -> bool:
    """Check if the position is within the bounds of the map."""

    return 0 <= position.x < len(area_map[0]) and 0 <= position.y < len(area_map)


def generate_route(
    area_map: Map,
    start_position: Optional[Position] = None,
    start_direction: Direction = Direction.North,
) -> Generator[Step]:
    """Calculate the steps of the guard's patrol route on the map."""

    position = start_position or find_start(area_map)
    direction = start_direction

    while True:
        yield Step(position, direction)

        next_position = direction.advance(position)
        if not is_valid_position(area_map, next_position):
            break

        if area_map[next_position.y][next_position.x] == OBSTACLE:
            direction = direction.rotate_clockwise()
            continue

        position = next_position


def count_distinct_visited_positions(
    area_map: Map,
    start_position: Optional[Position] = None,
    start_direction: Direction = Direction.North,
) -> int:
    """Count the number of distinct positions visited by the guard."""

    visited = {
        step.position
        for step in generate_route(area_map, start_position, start_direction)
    }

    return len(visited)


def count_obstruction_positions(
    area_map: Map,
    start_position: Optional[Position] = None,
    start_direction: Direction = Direction.North,
) -> int:
    """Count the positions where placing an obstruction would create an infinite loop.

    An obstruction can be placed at any position which would result in the
    guard retracing any part of their route.
    """

    obstruction_positions: set[Position] = set()
    previous_steps: set[Step] = set()

    for current_step, next_step in pairwise(
        generate_route(area_map, start_position, start_direction),
    ):
        previous_steps.add(current_step)
        if next_step.position in obstruction_positions:
            continue

        if next_step.position == current_step.position:
            continue

        rerouted_position = current_step.position
        rerouted_direction = current_step.direction.rotate_clockwise()
        rerouted_step = Step(rerouted_position, rerouted_direction)

        if will_create_infinite_loop(rerouted_step, previous_steps, area_map):
            obstruction_positions.add(next_step.position)

    return len(obstruction_positions)


def will_create_infinite_loop(
    start_step: Step,
    previous_steps: set[Step],
    area_map: Map,
) -> bool:
    """Determine if placing an obstruction at a position would create an infinite loop.

    This will occur if the guard's new route would retrace any of their previous steps.
    """

    previous_steps = previous_steps.copy()
    for step in generate_route(area_map, start_step.position, start_step.direction):
        if step in previous_steps:
            return True

        previous_steps.add(step)

    return False


def count_obstruction_positions_v2(
    area_map: Map,
    start_position: Optional[Position] = None,
    start_direction: Direction = Direction.North,
) -> int:
    previous_steps: set[Step] = set()
    loop_positions: set[Position] = set()

    for current_step, next_step in pairwise(
        generate_route(area_map, start_position, start_direction),
    ):
        previous_steps.add(current_step)

        rerouted_direction = current_step.direction.rotate_clockwise()
        rerouted_position = current_step.position
        rerouted_step = Step(rerouted_position, rerouted_direction)
        if will_create_infinite_loop(rerouted_step, previous_steps, area_map):
            loop_positions.add(next_step.position)

    return len(loop_positions)


def main() -> None:
    """Read information about a guard's patrol route and process it."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    area_map = read_map(file_path)

    start_position = find_start(area_map)

    distinct_visited_position_count = count_distinct_visited_positions(
        area_map,
        start_position,
    )
    print(distinct_visited_position_count)

    obstruction_position_count = count_obstruction_positions_v2(
        area_map,
        start_position,
    )
    print(obstruction_position_count)


if __name__ == "__main__":
    main()

# 296 is too low
# 2038 is wrong
# 2055 is too high
