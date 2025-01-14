"""
Advent of Code 2024, Day 19
Linen Layout
https://adventofcode.com/2024/day/19
"""

from functools import lru_cache
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def read_inputs(file_path: str) -> tuple[list[str], list[str]]:
    """Read patterns and desired designs from a file."""

    with open(file_path, encoding="utf-8") as file:
        lines = file.readlines()

    patterns = lines[0].strip().split(", ")
    designs = [line.strip() for line in lines[2:]]

    return patterns, designs


def can_create_design(design: str, patterns: list[str]) -> bool:
    """Determine if a design can be created from a selection of patterns."""

    if not patterns:
        return False

    @lru_cache
    def evaluate(current_design: str) -> bool:
        if not current_design:
            return True

        for pattern in patterns:
            if not current_design.startswith(pattern):
                continue

            remaining_design = current_design[len(pattern) :]
            if evaluate(remaining_design):
                return True

        return False

    return evaluate(design)


def count_ways_to_create_design(design: str, patterns: list[str]) -> int:
    """Count the number of ways to create a design from a selection of patterns."""

    if not patterns:
        return 0

    @lru_cache
    def evaluate(current_design: str) -> int:
        if not current_design:
            return 1

        ways = 0
        for pattern in patterns:
            if not current_design.startswith(pattern):
                continue

            remaining_design = current_design[len(pattern) :]
            ways += evaluate(remaining_design)

        return ways

    return evaluate(design)


def main() -> None:
    """Read patterns and desired designs from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    available_patterns, desired_designs = read_inputs(file_path)

    possible_design_count = sum(
        can_create_design(design, available_patterns) for design in desired_designs
    )
    print(possible_design_count)

    total_ways = sum(
        count_ways_to_create_design(design, available_patterns)
        for design in desired_designs
    )
    print(total_ways)


if __name__ == "__main__":
    main()
