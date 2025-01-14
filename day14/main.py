"""
Advent of Code 2024, Day 14
Restroom Redoubt
https://adventofcode.com/2024/day/14
"""

import re
from functools import reduce
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

DEFAULT_GRID_HEIGHT = 103
DEFAULT_GRID_WIDTH = 101
DEFAULT_SIMULATION_TIME = 100
ROBOT_INFO_REGEX = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


Grid = list[list[int]]


class Position(NamedTuple):
    """Represents a position relative to the top-left corner of the grid."""

    x: int
    y: int


class Velocity(NamedTuple):
    """Represents the velocity of a robot along the x and y axes."""

    dx: int
    dy: int


class RobotInfo(NamedTuple):
    """Describes the initial position and velocity of a robot."""

    initial_position: Position
    velocity: Velocity


class Quadrants(NamedTuple):
    """Represents the four quadrants of a grid."""

    top_left: Grid
    top_right: Grid
    bottom_left: Grid
    bottom_right: Grid


def read_robot_info(file_path: str) -> list[RobotInfo]:
    """Read the robot information from a file."""

    robots = []
    matches = re.findall(ROBOT_INFO_REGEX, open(file_path).read())

    for match in matches:
        x, y, dx, dy = map(int, match)
        robots.append(RobotInfo(Position(x, y), Velocity(dx, dy)))

    return robots


def count_final_positions(
    robots: list[RobotInfo],
    time: int = DEFAULT_SIMULATION_TIME,
    width: int = DEFAULT_GRID_WIDTH,
    height: int = DEFAULT_GRID_HEIGHT,
) -> Grid:
    """Count the number of robots in each cell of the grid after a given time."""

    grid = [[0] * width for _ in range(height)]

    for robot in robots:
        x, y = robot.initial_position
        dx, dy = robot.velocity

        calculated_x = x + dx * time
        calculated_y = y + dy * time

        actual_x = calculated_x % width
        actual_y = calculated_y % height

        grid[actual_y][actual_x] += 1

    return grid


def get_quadrants(grid: Grid) -> Quadrants:
    """Divide the grid into four quadrants.

    Values along the middle row and column are not included in any quadrant.
    """

    start_x, middle_x, end_x = 0, len(grid[0]) // 2, len(grid[0])
    start_y, middle_y, end_y = [0, len(grid) // 2, len(grid)]

    top_left = [row[start_x:middle_x] for row in grid[start_y:middle_y]]
    top_right = [row[middle_x + 1 : end_x] for row in grid[start_y:middle_y]]
    bottom_left = [row[start_x:middle_x] for row in grid[middle_y + 1 : end_y]]
    bottom_right = [row[middle_x + 1 : end_x] for row in grid[middle_y + 1 : end_y]]

    return Quadrants(top_left, top_right, bottom_left, bottom_right)


def safety_factor(grid: Grid) -> int:
    """Calculate the safety factor of the grid.

    The safety factor is the product of the number of robots in each quadrant of the
    grid. Any robots that are exactly in the middle of grid are not part of any
    quadrant and are not included in the calculation.
    """

    quadrants = get_quadrants(grid)
    quadrant_sums = [sum(sum(row) for row in quadrant) for quadrant in quadrants]

    return reduce(lambda x, y: x * y, quadrant_sums, 1)


def min_seconds_to_tree(
    robots: list[RobotInfo],
    width: int = DEFAULT_GRID_WIDTH,
    height: int = DEFAULT_GRID_HEIGHT,
) -> int:
    """Find the minimum number of seconds required for the robots to form a tree."""

    # NOTE: The intuition behind this solution is that the robots will likely form
    # the tree in the center of the grid, which would result in fewer robots in each
    # quadrant and therefore a lower safety factor. By running through the simulation
    # and checking the resulting frame whenever the safety factor decreases, we can
    # locate the frame where the tree is formed.

    current_time = 0
    time_at_min_safety_factor = 0
    min_safety_factor = 9999999999999999999999

    while current_time < 10000:
        current_time += 1
        grid = count_final_positions(robots, current_time, width, height)
        new_safety_factor = safety_factor(grid)

        if new_safety_factor >= min_safety_factor:
            continue

        min_safety_factor = new_safety_factor
        time_at_min_safety_factor = current_time
        print_grid(grid)

    return time_at_min_safety_factor


def print_grid(grid: Grid) -> None:
    """Print the grid to the console."""

    for row in grid:
        for cell in row:
            rep = "#" if cell else " "
            print(rep, end="")
        print()
    print()


def time_for_x_wraparound(velocity: Velocity, width: int) -> int:
    from math import gcd

    dx = velocity.dx

    if dx == 0:
        return 0

    return width // gcd(dx, width)


def time_for_y_wraparound(velocity: Velocity, height: int) -> int:
    from math import gcd

    dy = velocity.dy

    if dy == 0:
        return 0

    return height // gcd(dy, height)


def time_for_wraparound(velocity: Velocity, width: int, height: int) -> int:
    from math import lcm

    x_time = time_for_x_wraparound(velocity, width)
    y_time = time_for_y_wraparound(velocity, height)

    return lcm(x_time, y_time)


def main() -> None:
    """Read information about the guard robots from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    robots = read_robot_info(file_path)
    print(robots)

    grid = count_final_positions(robots)
    print(safety_factor(grid))

    min_time = min_seconds_to_tree(robots)
    print(min_time)

    # velocity = Velocity(3, 4)
    # width = 10
    # height = 6
    # print(time_for_x_wraparound(velocity, width))
    # print(time_for_y_wraparound(velocity, height))
    # print(time_for_wraparound(velocity, width, height))


if __name__ == "__main__":
    main()
