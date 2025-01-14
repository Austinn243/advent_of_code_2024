"""
Advent of Code 2024, Day 24
Crossed Wires
https://adventofcode.com/2024/day/24
"""

import re
from collections import defaultdict
from operator import iand, ior, ixor
from os import path
from pprint import pprint
from typing import Callable, NamedTuple, Optional

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"

CONSTANT_SIGNAL_REGEX = re.compile(r"(\w+): ([01])")
COMBINATION_SIGNAL_REGEX = re.compile(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)")

Operator = Callable[[int, int], int]

# Associates operator names with their corresponding functions.
OPERATOR_MAP: dict[str, Operator] = {
    "AND": iand,
    "OR": ior,
    "XOR": ixor,
}


class ConstantSignal(NamedTuple):
    """A signal that is a constant value."""

    name: str
    value: int

    def __repr__(self) -> str:
        """Convert the signal to a string for debugging."""

        return f"({self.name}: {self.value})"


class CompositeSignal(NamedTuple):
    """A signal that is derived from other signals."""

    input1_name: str
    input2_name: str
    output_name: str
    operator: Operator

    def __repr__(self) -> str:
        """Convert the signal to a string for debugging."""

        left_side = f"{self.input1_name} {self.operator.__name__} {self.input2_name}"
        return f"({left_side} -> {self.output_name})"


class Environment:
    """A simulation environment for signals."""

    def __init__(self) -> None:
        """Initialize the environment with empty signal data."""

        self.listeners: dict[str, list[SignalListener]] = defaultdict(list)
        self.values: dict[str, int] = {}

    def register(self, signal: CompositeSignal) -> None:
        """Register a signal that must be calculated from other signals."""

        listener = SignalListener(signal, self)

        self.listeners[signal.input1_name].append(listener)
        self.listeners[signal.input2_name].append(listener)

    def notify(self, constant_signal: ConstantSignal) -> None:
        """Notify listeners of a new constant signal."""

        name, value = constant_signal
        self.values[name] = value

        for listener in self.listeners[name]:
            listener.notify(constant_signal)


class SignalListener:
    """A listener for signals that must be calculated from other signals."""

    def __init__(self, signal: CompositeSignal, environment: Environment) -> None:
        """Create a new listener for a signal."""

        self.signal = signal
        self.environment = environment

        self.input1: Optional[ConstantSignal] = None
        self.input2: Optional[ConstantSignal] = None

    def notify(self, signal: ConstantSignal) -> None:
        """Receive a new signal and calculate the output signal."""

        if signal.name == self.signal.input1_name:
            self.input1 = signal
        elif signal.name == self.signal.input2_name:
            self.input2 = signal

        if not (self.input1 and self.input2):
            return

        value = self.signal.operator(self.input1.value, self.input2.value)
        self.environment.notify(ConstantSignal(self.signal.output_name, value))


def read_signals(
    file_path: str,
) -> tuple[list[ConstantSignal], list[CompositeSignal]]:
    """Read signal data from a file."""

    with open(file_path, encoding="utf-8") as file:
        lines = iter(file.readlines())

    constant_signals = []
    while line := next(lines).strip():
        match = CONSTANT_SIGNAL_REGEX.match(line)
        signal, value = match.groups()
        constant_signals.append(ConstantSignal(signal, int(value)))

    combination_signals = []
    for line in lines:
        match = COMBINATION_SIGNAL_REGEX.match(line)
        input1, operator_name, input2, output = match.groups()
        combination_signals.append(
            CompositeSignal(input1, input2, output, OPERATOR_MAP[operator_name]),
        )

    return constant_signals, combination_signals


def simulate_signals(
    constant_signals: list[ConstantSignal],
    combination_signals: list[CompositeSignal],
) -> dict[str, int]:
    """Simulate the signals to determine their values."""

    environment = Environment()
    for signal in combination_signals:
        environment.register(signal)

    for signal in constant_signals:
        environment.notify(signal)

    return environment.values


def combine_signal_bits_as_decimal(
    signal_prefix: str,
    signal_values: dict[str, int],
) -> int:
    """Combine the binary values of a group of signals into a decimal number."""

    z_signals = [
        (signal, value)
        for signal, value in signal_values.items()
        if signal.startswith(signal_prefix)
    ]
    z_signals.sort(key=lambda signal: int(signal[0][1:]), reverse=True)

    binary_value = "".join(str(value) for _, value in z_signals)

    return int(binary_value, 2)


def main() -> None:
    """Read signal data from a file and process it."""

    input_file = TEST_FILE_1
    file_path = path.join(path.dirname(__file__), input_file)

    constant_signals, combination_signals = read_signals(file_path)
    pprint(constant_signals)
    pprint(combination_signals)

    final_signals = simulate_signals(constant_signals, combination_signals)
    pprint(final_signals)

    prefix = "z"
    decimal_value = combine_signal_bits_as_decimal(prefix, final_signals)
    print(f"Decimal value of {prefix} signals: {decimal_value}")


if __name__ == "__main__":
    main()
