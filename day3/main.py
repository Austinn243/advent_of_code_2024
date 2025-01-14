"""
Advent of Code 2024 Day 3
Mull It Over
https://adventofcode.com/2024/day/3
"""

import re
from collections import namedtuple
from functools import partial
from heapq import heappop, heappush
from os import path
from typing import Callable

INPUT_FILE = "input.txt"

DO_INSTRUCTION_REGEX = r"do\(\)"
DONT_INSTRUCTION_REGEX = r"don't\(\)"
MULTIPLY_INSTRUCTION_REGEX = r"mul\((\d{1,3})\,(\d{1,3})\)"


Environment = namedtuple("Environment", ["total", "enabled"])
Instruction = Callable[[Environment], Environment]


def do(env: Environment) -> Environment:
    """Enable tracking of the total."""

    return Environment(env.total, True)


def dont(env: Environment) -> Environment:
    """Disable tracking of the total."""

    return Environment(env.total, False)


def multiply(env: Environment, x: int, y: int) -> Environment:
    """Multiply two numbers and add the result to the total."""

    if not env.enabled:
        return env

    return Environment(env.total + (x * y), env.enabled)


def is_multiply_instruction(instruction: Instruction) -> bool:
    """Determine if an instruction is a multiplication instruction."""

    return isinstance(instruction, partial) and instruction.func == multiply


def read_instructions(file_path: str) -> list[str]:
    """Read instructions from an input file."""

    with open(file_path, encoding="utf-8") as file:
        return file.readlines()


def parse_instructions(line: str) -> list[Instruction]:
    """Read the instructions from a line."""

    regex = [DO_INSTRUCTION_REGEX, DONT_INSTRUCTION_REGEX, MULTIPLY_INSTRUCTION_REGEX]

    instruction_heap = []
    for pattern in regex:
        for match in re.finditer(pattern, line):
            instruction = None
            if pattern == DO_INSTRUCTION_REGEX:
                instruction = do
            if pattern == DONT_INSTRUCTION_REGEX:
                instruction = dont
            if pattern == MULTIPLY_INSTRUCTION_REGEX:
                x, y = map(int, match.groups())
                instruction = partial(multiply, x=x, y=y)

            heappush(instruction_heap, (match.start(), instruction))

    instructions = []
    while instruction_heap:
        _, instruction = heappop(instruction_heap)
        instructions.append(instruction)

    return instructions


def evaluate_instructions(instructions: Instruction) -> int:
    """Evaluate all instructions in a batch, returning the total."""

    env = Environment(enabled=True, total=0)

    for instruction in instructions:
        env = instruction(env)

    return env.total


def flat_map[T, U](func: Callable[T, list[U]], iterable: list[T]) -> list[U]:
    """Map a function over an iterable and flatten the result."""

    return [result for item in iterable for result in func(item)]


def main() -> None:
    """Read instructions from a file and evaluate them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    lines = read_instructions(file_path)

    instructions = flat_map(parse_instructions, lines)

    multiplication_instructions = [
        instruction
        for instruction in instructions
        if is_multiply_instruction(instruction)
    ]
    multiplication_only_total = evaluate_instructions(multiplication_instructions)
    print(multiplication_only_total)

    overall_instructions_total = evaluate_instructions(instructions)
    print(overall_instructions_total)


if __name__ == "__main__":
    main()
