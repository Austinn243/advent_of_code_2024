"""
Advent of Code 2024: Day 1
Historian Hysteria
https://adventofcode.com/2024/day/1
"""

from collections import Counter
from os import path

INPUT_FILE = "input.txt"


def read_inputs(file_path: str) -> tuple[list[int], list[int]]:
    """Read the pair of integers from each line and group them into separate lists."""

    left = []
    right = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            num1, num2 = map(int, line.strip().split())
            left.append(num1)
            right.append(num2)

    return left, right


def sum_of_min_differences(left: list[int], right: list[int]) -> int:
    """Calculate the sum of the smallest differences between values in two lists."""

    return sum(abs(x - y) for x, y in zip(sorted(left), sorted(right)))


def similarity_score(left: list[int], right: list[int]) -> int:
    """Calculate the similarity score between two lists of integers.

    The similarity score is the sum of each value in the left list it
    has been multiplied by its frequency in the right list.
    """

    keys = set(left)
    frequencies = Counter(right)

    return sum(key * frequencies.get(key, 0) for key in keys)


def main() -> None:
    """Read pairs of numbers from a file and process them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    left, right = read_inputs(file_path)

    print(sum_of_min_differences(left, right))
    print(similarity_score(left, right))


if __name__ == "__main__":
    main()
