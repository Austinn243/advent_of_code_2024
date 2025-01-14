"""
Advent of Code 2024, Day 17
Chronospatial Computer
https://adventofcode.com/2024/day/17
"""

import re
from dataclasses import dataclass
from os import path
from typing import Callable, NamedTuple, Optional

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"
PROGRAM_REGEX = re.compile(r"Program: (.+)")
REGISTER_REGEX = re.compile(r"Register [ABC]: (\d+)")


class Registry(NamedTuple):
    """Contains registers for reading and writing values."""

    a: int
    b: int
    c: int


@dataclass
class Environment:
    """Manages the execution environment for the program."""

    def __init__(
        self,
        registry: Registry,
        instruction_pointer: int = 0,
        output: Optional[list[int]] = None,
    ) -> None:
        """Create a new execution environment."""

        self._registry = registry
        self._instruction_pointer = instruction_pointer
        self._output = output or []

    @property
    def output(self) -> list:
        """Retrieves the output of the program."""

        return self._output

    @property
    def registry(self) -> Registry:
        """Retrieves the registry of the environment."""

        return self._registry

    @property
    def instruction_pointer(self) -> int:
        """Retrieves the current instruction pointer."""

        return self._instruction_pointer


OpCode = int
Operand = int
Instruction = Callable[[Operand, Environment], Environment]
Program = list[int]


def read_inputs(file_path: str) -> tuple[Registry, Program]:
    """Read the input file and return the registry and program."""

    with open(file_path, encoding="utf-8") as file:
        lines = file.readlines()

    registry_lines = lines[:3]
    registry_values = []
    for line in registry_lines:
        match = REGISTER_REGEX.match(line)
        if not match:
            raise ValueError("Invalid registry line")

        registry_values.append(int(match.group(1)))

    registry = Registry(*registry_values)

    program_line = lines[4]
    match = PROGRAM_REGEX.match(program_line)
    if not match:
        raise ValueError("Invalid program line")

    program = [int(value) for value in match.group(1).split(",")]

    return registry, program


def evaluate_literal_operand(operand: Operand) -> int:
    """Evaluate a literal operand and return the value."""

    return operand


def evaluate_combo_operand(operand: int, registry: Registry) -> int:
    """Evaluate a combo operand and return the value."""

    if operand in [0, 1, 2, 3]:
        return operand
    if operand == 4:
        return registry.a
    if operand == 5:
        return registry.b
    if operand == 6:
        return registry.c
    if operand == 7:
        raise ValueError("Combo operand 7 is reserved and not for use in programs")

    raise ValueError("Unknown combo operand")


def increment_instruction_pointer(instruction_pointer: int) -> int:
    """Update the instruction pointer to the next instruction."""

    # NOTE: The program lists each instruction followed by its operand.
    # In order to move to the next instruction, we therefore need to add 2.
    return instruction_pointer + 2


def update_a_register(registry: Registry, value: int) -> Registry:
    """Update the A register with the given value."""

    return Registry(value, registry.b, registry.c)


def update_b_register(registry: Registry, value: int) -> Registry:
    """Update the B register with the given value."""

    return Registry(registry.a, value, registry.c)


def update_c_register(registry: Registry, value: int) -> Registry:
    """Update the C register with the given value."""

    return Registry(registry.a, registry.b, value)


def adv(operand: int, env: Environment) -> Environment:
    """Divide the value in register A and write the result to register A."""

    numerator = env.registry.a
    denominator = 2 ** evaluate_combo_operand(operand, env.registry)

    quotient = numerator // denominator

    updated_registry = update_a_register(env.registry, quotient)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def bxl(operand: Operand, env: Environment) -> Environment:
    """XOR the value in register B and write the result to register B."""

    operand_value = evaluate_literal_operand(operand)

    result = env.registry.b ^ operand_value

    updated_registry = update_b_register(env.registry, result)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def bst(operand: Operand, env: Environment) -> Environment:
    """Modulo the value in register B by 8 and write the result to register B."""

    operand_value = evaluate_combo_operand(operand, env.registry)

    result = operand_value % 8

    updated_registry = update_b_register(env.registry, result)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def jnz(operand: Operand, env: Environment) -> Environment:
    """Jump to the given instruction if the value in register A is not zero."""

    updated_instruction_pointer = (
        evaluate_literal_operand(operand)
        if env.registry.a != 0
        else increment_instruction_pointer(env.instruction_pointer)
    )

    return Environment(env.registry, updated_instruction_pointer, env.output)


def bxc(_: Operand, env: Environment) -> Environment:
    """XOR the values in registers B and C and write the result to register B."""

    result = env.registry.b ^ env.registry.c

    updated_registry = update_b_register(env.registry, result)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def out(operand: Operand, env: Environment) -> Environment:
    """Modulo the operand by 8 and append the result to the output."""

    operand_value = evaluate_combo_operand(operand, env.registry)
    result = operand_value % 8

    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)
    updated_output = env.output.copy()
    updated_output.append(result)

    return Environment(env.registry, updated_instruction_pointer, updated_output)


def bdv(operand: int, env: Environment) -> Environment:
    """Divide the value in register A and write the result to register B."""

    numerator = env.registry.a
    denominator = 2 ** evaluate_combo_operand(operand, env.registry)

    quotient = numerator // denominator

    updated_registry = update_b_register(env.registry, quotient)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def cdv(operand: int, env: Environment) -> Environment:
    """Divide the value in register A and write the result to register C."""

    numerator = env.registry.a
    denominator = 2 ** evaluate_combo_operand(operand, env.registry)

    quotient = numerator // denominator

    updated_registry = update_c_register(env.registry, quotient)
    updated_instruction_pointer = increment_instruction_pointer(env.instruction_pointer)

    return Environment(updated_registry, updated_instruction_pointer, env.output)


def execute(
    program: Program,
    instructions: dict[OpCode, Instruction],
    env: Environment,
) -> Environment:
    """Execute the given program using the provided instructions and environment."""

    updated_env = env
    while updated_env.instruction_pointer < len(program) - 1:
        op_code = program[updated_env.instruction_pointer]
        operand = program[updated_env.instruction_pointer + 1]

        updated_env = instructions[op_code](operand, updated_env)

    return updated_env


def main() -> None:
    """Read information from the input file and execute the program."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    registry, program = read_inputs(file_path)

    env = Environment(registry)

    operations: dict[OpCode, Instruction] = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    updated_env = execute(program, operations, env)
    print(updated_env.output)


if __name__ == "__main__":
    main()
