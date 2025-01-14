"""
Advent of Code 2024, Day 25
Code Chronicle
https://adventofcode.com/2024/day/25
"""

from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

EMPTY = "."
FILLED = "#"
SCHEMATIC_HEIGHT = 7
SCHEMATIC_WIDTH = 5

Schematic = list[int]


def parse_schematic(raw_schematic: list[str]) -> Schematic:
    """Parse a schematic from a list of strings."""

    schematic = [0] * SCHEMATIC_WIDTH

    for row in raw_schematic:
        for i, char in enumerate(row):
            if char == FILLED:
                schematic[i] += 1

    return schematic


def is_lock_schematic(raw_schematic: list[str]) -> bool:
    """Determine if a schematic represents a lock."""

    return raw_schematic[0][0] == EMPTY


def is_key_schematic(schematic: Schematic) -> bool:
    """Determine if a schematic represents a key."""

    return not is_lock_schematic(schematic)


def read_schematics(file_path: str) -> tuple[list[Schematic], list[Schematic]]:
    """Read lock and key schematics from a file and return them in that order."""

    raw_schematics = []
    current_raw_schematic = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                raw_schematics.append(current_raw_schematic)
                current_raw_schematic = []
                continue

            current_raw_schematic.append(line)

    if current_raw_schematic:
        raw_schematics.append(current_raw_schematic)

    locks = [
        parse_schematic(schematic)
        for schematic in raw_schematics
        if is_lock_schematic(schematic)
    ]
    keys = [
        parse_schematic(schematic)
        for schematic in raw_schematics
        if is_key_schematic(schematic)
    ]

    return locks, keys


def lock_matches_key(lock: Schematic, key: Schematic) -> bool:
    """Determine if a lock matches a key."""

    return all(lock[i] + key[i] <= SCHEMATIC_HEIGHT for i in range(SCHEMATIC_WIDTH))


def count_key_lock_matches(locks: list[Schematic], keys: list[Schematic]) -> int:
    """Count the number of key-lock matches."""

    return sum(lock_matches_key(lock, key) for lock in locks for key in keys)


def main() -> None:
    """Read key and lock schematics from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    locks, keys = read_schematics(file_path)
    print(locks)
    print(keys)

    match_count = count_key_lock_matches(locks, keys)
    print(match_count)


if __name__ == "__main__":
    main()
