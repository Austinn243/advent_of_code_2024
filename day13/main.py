"""
Advent of Code 2024, Day 13
Claw Contraption
https://adventofcode.com/2024/day/13
"""

import re
from os import path
from typing import NamedTuple, Optional

from sympy import Eq, symbols
from sympy.solvers import solve

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

A_BUTTON_PRESS_COST = 3
B_BUTTON_PRESS_COST = 1
CLAW_REGEX = re.compile(
    (
        r"Button A: X\+(\d+), Y\+(\d+)\s"
        r"Button B: X\+(\d+), Y\+(\d+)\s"
        r"Prize: X=(\d+), Y=(\d+)"
    ),
)


class ButtonConfiguration(NamedTuple):
    """Describes the effects of pressing a button."""

    x_offset: int
    y_offset: int


class Position(NamedTuple):
    """Indicates a position in the claw machine."""

    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        """Add two positions together."""

        return Position(self.x + other.x, self.y + other.y)


class ClawMachineConfiguration(NamedTuple):
    """Describes a claw machine configuration."""

    button_a: ButtonConfiguration
    button_b: ButtonConfiguration
    prize_position: Position


def read_claw_machine_configurations(file_path: str) -> list[ClawMachineConfiguration]:
    """Read information about claw machines from a file."""

    matches = re.findall(CLAW_REGEX, open(file_path).read())

    configurations = []
    for match in matches:
        ax, ay, bx, by, px, py = map(int, match)

        button_a = ButtonConfiguration(ax, ay)
        button_b = ButtonConfiguration(bx, by)
        prize = Position(px, py)

        configurations.append(ClawMachineConfiguration(button_a, button_b, prize))

    return configurations


def min_cost_to_prize(
    configuration: ClawMachineConfiguration,
    a_button_press_cost: int = A_BUTTON_PRESS_COST,
    b_button_press_cost: int = B_BUTTON_PRESS_COST,
) -> Optional[int]:
    """Calculate the minimum token cost to reach the prize.

    Returns None if the prize is unreachable.
    """

    a, b = symbols("a b")

    ax, ay = configuration.button_a
    bx, by = configuration.button_b
    px, py = configuration.prize_position

    equation1 = Eq(a * ax + b * bx, px)
    equation2 = Eq(a * ay + b * by, py)

    # NOTE: Every system of equations here will have a solution but it isn't guaranteed
    # to be an integer solution. We cannot have a fraction of a button press so any
    # system of equations that doesn't have an integer solution is invalid.

    solution = solve((equation1, equation2), (a, b), dict=True)[0]

    all_presses_are_integers = all(value.is_Integer for value in solution.values())
    if not all_presses_are_integers:
        return None

    a_press_count = solution[a]
    b_press_count = solution[b]

    return a_press_count * a_button_press_cost + b_press_count * b_button_press_cost


def sum_min_costs_to_prizes(configurations: list[ClawMachineConfiguration]) -> int:
    """Calculate the sum of the minimum costs to reach the prizes."""

    return sum(min_cost_to_prize(cfg) or 0 for cfg in configurations)


def apply_correction_to_configuration(
    configuration: ClawMachineConfiguration,
    correction: Position,
) -> ClawMachineConfiguration:
    """Apply a correction to a claw machine configuration."""

    corrected_prize_position = configuration.prize_position + correction

    return ClawMachineConfiguration(
        configuration.button_a,
        configuration.button_b,
        corrected_prize_position,
    )


def main() -> None:
    """Read claw machine configurations from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    claw_machine_configurations = read_claw_machine_configurations(file_path)

    print(sum_min_costs_to_prizes(claw_machine_configurations))

    corrected_configurations = [
        apply_correction_to_configuration(cfg, Position(10000000000000, 10000000000000))
        for cfg in claw_machine_configurations
    ]
    print(sum_min_costs_to_prizes(corrected_configurations))


if __name__ == "__main__":
    main()
