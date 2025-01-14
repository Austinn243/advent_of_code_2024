"""
Advent of Code 2024, Day 22
Monkey Market
https://adventofcode.com/2024/day/22
"""

from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"
PRUNE_NUMBER = 16777216


def read_secret_numbers(file_path: str) -> list[int]:
    """Read the secret numbers from a file."""

    with open(file_path) as file:
        return [int(line.strip()) for line in file]


def mix(secret_number: int, mix_number: int) -> int:
    """Mix a value into the secret number."""

    return secret_number ^ mix_number


def prune(secret_number: int) -> int:
    """Prune the secret number."""

    return secret_number % PRUNE_NUMBER


def generate_next_secret_number(secret_number: int) -> int:
    """Generate the next secret number."""

    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, secret_number // 32))
    secret_number = prune(mix(secret_number, secret_number * 2048))

    return secret_number


def generate_nth_secret_number(secret_number: int, n: int) -> int:
    """Generate the nth secret number."""

    for _ in range(n):
        secret_number = generate_next_secret_number(secret_number)

    return secret_number


def main() -> None:
    """Read the secret numbers from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    secret_numbers = read_secret_numbers(file_path)
    print(secret_numbers)
    print(generate_nth_secret_number(123, 10))

    two_thousandth_secret_numbers = [
        generate_nth_secret_number(secret_number, 2000)
        for secret_number in secret_numbers
    ]
    print(two_thousandth_secret_numbers)
    print(sum(two_thousandth_secret_numbers))


if __name__ == "__main__":
    main()
