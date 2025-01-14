"""
Advent of Code 2024, Day 11
Plutonian Pebbles
https://adventofcode.com/2024/day/11
"""

from collections import Counter
from functools import cache
from math import log10
from os import path

# NOTE: The problem states that the stones maintain their relative ordering
# after each blink, which would insinuate that the ordering of the stones
# matters. However, we are only concerned in the total number of stones after
# each set of blinks, not the resulting stones themselves. Therefore, we can
# ignore the ordering of the stones and only keep track of the number of each
# stone, significantly reducing the complexity of the problem.

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

Stone = int


def read_stones(file_path: str) -> list[Stone]:
    """Read the stones from the file."""

    with open(file_path, encoding="utf-8") as file:
        return [int(num) for num in file.read().split()]


@cache
def blink(stone: Stone) -> list[Stone]:
    """Blink a stone once and return the new stones it generates."""

    if stone == 0:
        return [1]

    digit_count = int(log10(stone)) + 1
    if digit_count % 2 == 0:
        half_digit_count = digit_count // 2

        left_part = stone // (10**half_digit_count)
        right_part = stone % (10**half_digit_count)

        return [left_part, right_part]

    return [stone * 2024]


def count_stones_after_n_blinks(stones: list[Stone], blink_count: int) -> int:
    """Blink a specified number of times and return the total number of stones."""

    stone_counts = Counter(stones)

    for _ in range(blink_count):
        new_stone_counts = Counter()

        for stone, count in stone_counts.items():
            new_stones = blink(stone)

            for new_stone in new_stones:
                new_stone_counts[new_stone] += count

        stone_counts = new_stone_counts

    return sum(stone_counts.values())


def main() -> None:
    """Read information about the stones and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    stones = read_stones(file_path)
    print(stones)

    stone_count_after_25 = count_stones_after_n_blinks(stones, 25)
    print(stone_count_after_25)

    stone_count_after_75 = count_stones_after_n_blinks(stones, 75)
    print(stone_count_after_75)


if __name__ == "__main__":
    main()
