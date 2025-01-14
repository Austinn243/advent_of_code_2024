"""
Advent of Code 2024, Day 4
Ceres Search
https://adventofcode.com/2024/day/4
"""

from collections import namedtuple
from collections.abc import Generator
from itertools import product
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

ALL_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
]

Position = namedtuple("Position", ["row", "column"])
WordSearch = list[str]


def read_word_search(file_path: str) -> WordSearch:
    """Read the word search from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [line.strip() for line in file]


def positions(word_search: WordSearch) -> Generator[Position]:
    """Generate all possible positions in the word search."""

    row_count = len(word_search)
    column_count = len(word_search[0])

    for row, column in product(range(row_count), range(column_count)):
        yield Position(row, column)


def count_word_occurrences(word_search: WordSearch, word: str) -> int:
    """Count the number of times the specified word appears in the word search."""

    return sum(
        count_word_occurrences_at_position(word_search, word, position)
        for position in positions(word_search)
    )


def is_within_bounds(word_search: WordSearch, position: Position) -> bool:
    """Determine if a position is within the bounds of the word search."""

    is_valid_row = 0 <= position.row < len(word_search)
    is_valid_column = 0 <= position.column < len(word_search[0])

    return is_valid_row and is_valid_column


def count_word_occurrences_at_position(
    word_search: WordSearch,
    word: str,
    position: Position,
) -> int:
    """Count how many times a word appears starting at a given position."""

    def evaluate_letter(
        position: Position,
        letter_index: int,
        directions: list[tuple[int, int]],
    ) -> bool:
        if letter_index >= len(word):
            return True

        if not is_within_bounds(word_search, position):
            return False

        letter_to_match = word[letter_index]
        letter_at_position = word_search[position.row][position.column]

        if letter_at_position != letter_to_match:
            return False

        return sum(
            evaluate_letter(
                Position(position.row + direction[0], position.column + direction[1]),
                letter_index + 1,
                [direction],
            )
            for direction in directions
        )

    return evaluate_letter(
        position,
        letter_index=0,
        directions=ALL_DIRECTIONS,
    )


def is_cross_at_position(word_search: WordSearch, position: Position) -> bool:
    """Determine if 'MAS' appears in a cross shape at a given position."""

    if word_search[position.row][position.column] != "A":
        return False

    diagonal_neighbors = [
        Position(position.row - 1, position.column - 1),
        Position(position.row - 1, position.column + 1),
        Position(position.row + 1, position.column + 1),
        Position(position.row + 1, position.column - 1),
    ]

    if not all(
        is_within_bounds(word_search, position) for position in diagonal_neighbors
    ):
        return False

    top_left, top_right, bottom_right, bottom_left = (
        word_search[p.row][p.column] for p in diagonal_neighbors
    )

    return any(
        [
            top_left == top_right == "M" and bottom_left == bottom_right == "S",
            top_left == bottom_left == "M" and top_right == bottom_right == "S",
            top_right == bottom_right == "M" and top_left == bottom_left == "S",
            bottom_left == bottom_right == "M" and top_left == top_right == "S",
        ],
    )


def count_xmas_crosses(word_search: WordSearch) -> int:
    """Count how many times 'MAS' appears in a cross shape in the word search."""

    return sum(
        is_cross_at_position(word_search, position)
        for position in positions(word_search)
    )


def main() -> None:
    """Read the word search from a file and process it."""

    input_file_path = path.join(path.dirname(__file__), INPUT_FILE)
    # test_file_path = path.join(path.dirname(__file__), TEST_FILE)

    word_search = read_word_search(input_file_path)

    xmas_word_count = count_word_occurrences(word_search, "XMAS")
    print(xmas_word_count)

    xmas_cross_count = count_xmas_crosses(word_search)
    print(xmas_cross_count)


if __name__ == "__main__":
    main()
