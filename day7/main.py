"""
Advent of Code 2024, Day 7
Bridge Repair
https://adventofcode.com/2024/day/7
"""

import re
from dataclasses import dataclass
from operator import add, mul
from os import path
from typing import Callable

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

NUMBER_REGEX = r"\d+"


Operator = Callable[[int, int], int]


@dataclass
class Equation:
    """An equation with operands and a result."""

    def __init__(self, operands: list[int], result: int) -> None:
        """Create a new equation with the specified operands and result."""

        self.operands = operands
        self.result = result

    def __repr__(self) -> str:
        """Return a string representation of the equation."""

        operands = " ".join(map(str, self.operands))
        return f"{self.result}: {operands}"

    def is_possible(self, operators: list[Operator]) -> bool:
        """Determine if the equation is possible.

        An equation is possible if the result can be obtained by adding or
        multiplying the operands together in order from left to right,
        regardless of precedence.
        """

        if len(self.operands) == 1:
            return self.operands[0] == self.result

        operand1, operand2, *rest = self.operands
        new_operands = [op(operand1, operand2) for op in operators]

        equations = [
            Equation([operand, *rest], self.result) for operand in new_operands
        ]

        return any(equation.is_possible(operators) for equation in equations)

    def calibration_value(self) -> int:
        """Calculate the calibration value of the equation."""

        return self.result


def concatenate(a: int, b: int) -> int:
    """Concatenate two numbers together."""

    return int(str(a) + str(b))


def read_equations(file_path: str) -> list[Equation]:
    """Read equations from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_equation(line) for line in file]


def parse_equation(line: str) -> Equation:
    """Parse an equation from a line of text."""

    matches = re.findall(NUMBER_REGEX, line)
    values = map(int, matches)

    result, *operands = values
    return Equation(operands, result)


def main() -> None:
    """Read equations from an input file and process them."""

    file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), file)

    equations = read_equations(file_path)

    operator_groups = [[add, mul], [add, mul, concatenate]]
    for operators in operator_groups:
        possible_equations = [
            equation for equation in equations if equation.is_possible(operators)
        ]
        total_calibration_value = sum(
            equation.calibration_value() for equation in possible_equations
        )
        print(total_calibration_value)


if __name__ == "__main__":
    main()
