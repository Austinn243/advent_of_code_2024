"""
Advent of Code 2024, Day 18
RAM Run
https://adventofcode.com/2024/day/18
"""

from enum import Enum
from heapq import heappop, heappush
from os import path
from typing import NamedTuple, Optional

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

DEFAULT_MEMORY_SPACE_WIDTH = 71
DEFAULT_MEMORY_SPACE_HEIGHT = 71


class Position(NamedTuple):
    """A byte position in memory."""

    x: int
    y: int


class Byte(Enum):
    """Represents the state of a byte in memory."""

    SAFE = "."
    CORRUPTED = "#"


MemorySpace = list[list[Byte]]


def read_byte_positions(file_path: str) -> list[Position]:
    """Read byte positions from a file."""

    positions = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            x, y = map(int, line.strip().split(","))
            positions.append(Position(x, y))

    return positions


def create_memory_space(
    width: int = DEFAULT_MEMORY_SPACE_WIDTH,
    height: int = DEFAULT_MEMORY_SPACE_HEIGHT,
) -> MemorySpace:
    """Create a memory space with the given dimensions."""

    return [[Byte.SAFE for _ in range(width)] for _ in range(height)]


def drop_bytes(
    byte_positions: list[Position],
    memory_space: Optional[MemorySpace] = None,
) -> MemorySpace:
    """Drop bytes into a memory space with the given dimensions."""

    memory_space = memory_space.copy() if memory_space else create_memory_space()

    for x, y in byte_positions:
        memory_space[y][x] = Byte.CORRUPTED

    return memory_space


def is_within_bounds(position: Position, memory_space: MemorySpace) -> bool:
    """Check if a position is within the bounds of a memory space."""

    x, y = position

    return 0 <= x < len(memory_space[0]) and 0 <= y < len(memory_space)


def find_visitable_neighbors(
    position: Position,
    memory_space: MemorySpace,
) -> list[Position]:
    """Find the neighbors of a position in a memory space that can be visited."""

    neighbors = [
        Position(position.x - 1, position.y),
        Position(position.x + 1, position.y),
        Position(position.x, position.y - 1),
        Position(position.x, position.y + 1),
    ]

    return [
        neighbor
        for neighbor in neighbors
        if is_within_bounds(neighbor, memory_space)
        and memory_space[neighbor.y][neighbor.x] == Byte.SAFE
    ]


def count_min_steps_to_exit(memory_space: MemorySpace) -> int:
    """Find the minimum number of steps required to exit the memory space."""

    start_position = Position(0, 0)
    end_position = Position(len(memory_space[0]) - 1, len(memory_space) - 1)

    visited = set()
    queue = [(0, start_position)]

    while queue:
        step_count, position = heappop(queue)
        if position == end_position:
            return step_count

        if position in visited:
            continue

        visited.add(position)

        for neighbor in find_visitable_neighbors(position, memory_space):
            heappush(queue, (step_count + 1, neighbor))

    raise ValueError("No path to exit the memory space.")


def find_blocking_byte_position(
    byte_positions: list[Position],
    memory_space: MemorySpace,
) -> Position:
    """Find the byte position that blocks the exit of the memory space."""

    # This does work to find a byte that blocks the exit but it isn't returning
    # the correct answer for the main case. Since we're going in reverse order
    # and returning the first byte that blocks the exit, it might be because
    # there is a byte that drops earlier that blocks the exit, which is what
    # the question is asking for.

    end_position = Position(0, 0)

    visited = set()

    def sweep(position: Position) -> bool:
        if position == end_position:
            return True

        if position in visited:
            return False

        visited.add(position)

        return any(
            sweep(neighbor)
            for neighbor in find_visitable_neighbors(position, memory_space)
        )

    for candidate in reversed(byte_positions):
        memory_space[candidate.y][candidate.x] = Byte.SAFE

        if sweep(candidate):
            return candidate

    raise ValueError("No blocking byte position found.")


def print_memory_space(memory_space: MemorySpace) -> None:
    """Print a memory space."""

    for row in memory_space:
        print("".join(byte.value for byte in row))


def run_test() -> None:
    """Run the test case for the program."""

    file_path = path.join(path.dirname(__file__), TEST_FILE)

    byte_positions = read_byte_positions(file_path)
    print(byte_positions)

    memory_space = create_memory_space(7, 7)
    partial_memory_space = drop_bytes(byte_positions[:-2], memory_space)

    min_step_count = count_min_steps_to_exit(partial_memory_space)
    print(min_step_count)

    final_memory_space = drop_bytes(byte_positions[-2:], partial_memory_space)
    blocking_byte_position = find_blocking_byte_position(
        byte_positions,
        final_memory_space,
    )
    print(blocking_byte_position)


def main() -> None:
    """Read byte positions from an input file and process them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    byte_positions = read_byte_positions(file_path)

    memory_space = create_memory_space()
    partial_memory_space = drop_bytes(byte_positions[:1024], memory_space)

    min_step_count = count_min_steps_to_exit(partial_memory_space)
    print(min_step_count)

    final_memory_space = drop_bytes(byte_positions[1024:], partial_memory_space)
    blocking_byte_position = find_blocking_byte_position(
        byte_positions,
        final_memory_space,
    )
    print(blocking_byte_position)


if __name__ == "__main__":
    run_test()
    main()
