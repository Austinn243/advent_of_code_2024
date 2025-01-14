"""
Advent of Code 2024, Day 16
Reindeer Maze
https://adventofcode.com/2024/day/16
"""

from enum import Enum
from heapq import heappop, heappush
from os import path
from time import perf_counter
from typing import Callable, NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"


class Cell(Enum):
    """Represents the contents of a position in the maze."""

    START = "S"
    END = "E"
    EMPTY = "."
    WALL = "#"

    def __str__(self) -> str:
        """Convert the cell to a user-friendly string representation."""

        return self.value


class Position(NamedTuple):
    """Represents a position in the maze."""

    x: int
    y: int


class Direction(Enum):
    """Represents a direction of movement in the maze."""

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def advance(self, position: Position) -> Position:
        """Advance the position in this direction."""

        dx, dy = self.value

        return Position(position.x + dx, position.y + dy)

    def turn_clockwise(self) -> "Direction":
        """Turn 90 degrees clockwise and return the new direction."""

        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

    def turn_counter_clockwise(self) -> "Direction":
        """Turn 90 degrees counter-clockwise and return the new direction."""

        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.WEST:
                return Direction.SOUTH


Maze = list[list[Cell]]

DEFAULT_STARTING_DIRECTION = Direction.EAST
DEFAULT_MOVE_COST = 1
DEFAULT_TURN_COST = 1000


def interpret_char_as_cell(char: str) -> Cell:
    """Interpret a character as a cell in the maze."""

    if char == Cell.START.value:
        return Cell.START
    elif char == Cell.END.value:
        return Cell.END
    elif char == Cell.EMPTY.value:
        return Cell.EMPTY
    elif char == Cell.WALL.value:
        return Cell.WALL
    else:
        raise ValueError(f"Unknown cell character: {char}")


def read_maze(file_path: str) -> Maze:
    """Read the maze layout from the input file and parse it."""

    maze = []
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            row = [interpret_char_as_cell(char) for char in line.strip()]

            maze.append(row)

    return maze


def print_maze(maze: Maze) -> None:
    """Print the maze layout to the console."""

    for row in maze:
        for cell in row:
            print(cell, end="")
        print()


def find_start_position(maze: Maze) -> Position:
    """Find the starting position in the maze."""

    return Position(1, len(maze) - 2)


def find_end_position(maze: Maze) -> Position:
    """Find the ending position in the maze."""

    return Position(len(maze[0]) - 2, 1)


def is_within_bounds(maze: Maze, position: Position) -> bool:
    """Check if the position is within the bounds of the maze."""

    return 0 <= position.x < len(maze[0]) and 0 <= position.y < len(maze)


def create_counter(start: int) -> Callable[[], int]:
    """Create a counter function that starts at the given value."""

    counter = start - 1

    def increment() -> int:
        nonlocal counter
        counter += 1
        return counter

    return increment


def min_cost_to_end(
    maze: Maze,
    start_direction: Direction = DEFAULT_STARTING_DIRECTION,
    move_cost: int = DEFAULT_MOVE_COST,
    turn_cost: int = DEFAULT_TURN_COST,
) -> int:
    """Calculate the minimum cost to reach the end of the maze."""

    start_position = find_start_position(maze)
    end_position = find_end_position(maze)

    print(start_position)
    print(end_position)

    count = create_counter(0)
    queue = [(0, count(), start_position, start_direction)]
    visited = set()

    while queue:
        cost, _, position, direction = heappop(queue)
        if position == end_position:
            return cost

        if position in visited:
            continue

        visited.add(position)
        if maze[position.y][position.x] == Cell.WALL:
            continue

        left_direction = direction.turn_counter_clockwise()
        right_direction = direction.turn_clockwise()

        left_position = left_direction.advance(position)
        forward_position = direction.advance(position)
        right_position = right_direction.advance(position)

        move_forward_cost = cost + move_cost
        move_side_cost = turn_cost + move_forward_cost

        left_step = (
            move_side_cost,
            count(),
            left_position,
            left_direction,
        )
        forward_step = (
            move_forward_cost,
            count(),
            forward_position,
            direction,
        )
        right_step = (
            move_side_cost,
            count(),
            right_position,
            right_direction,
        )

        heappush(queue, left_step)
        heappush(queue, forward_step)
        heappush(queue, right_step)

    raise ValueError("No path to the end of the maze found.")


def count_best_path_tiles(
    maze: Maze,
    start_direction: Direction = DEFAULT_STARTING_DIRECTION,
    move_cost: int = DEFAULT_MOVE_COST,
    turn_cost: int = DEFAULT_TURN_COST,
) -> int:
    """Count the number of tiles that are on any of the best paths through the maze."""

    start_position = find_start_position(maze)
    end_position = find_end_position(maze)

    print(start_position)
    print(end_position)

    count = create_counter(0)
    queue = [(0, count(), start_position, start_direction, None)]

    # We use a sentinel value for the end position to simplify best path logic.
    min_cost_to_position = {
        end_position: 999999999,
    }

    best_paths = []

    # Since we're using a variant of Dijkstra's algorithm, we know that the first path
    # to reach the end will be one of the shortest/best paths. This means that we can
    # track the number of tiles visited by this path and then use it to determine which
    # of the remaining paths are also best paths. Any path that exceeds this count can
    # be terminated early, saving time and memory.

    # All the paths will have some crossover so using a set to eliminate duplicates
    # might not be the best idea. One thing we could try is including the previous
    # position for any given node in the queue. With this, we could keep track of the
    # last nodes of each best path and then unwind them to recreate the paths.

    # FIXME: The reason that we're not getting the correct answer with any of our
    # implementations is because some nodes are being excluded too early from the
    # search because they have a higher initial cost than previously encountered
    # due to the turn and move costs being accounted for in one step rather than
    # separate steps. In the first example, the additional paths on the left side
    # are excluded because the cost of reaching the last intersection is higher
    # than the cost of reaching it from the right side. This is because they have
    # already turned and moved toward the end position whereas the right side
    # path has yet to do so. As a result, their cost is greater than the right side
    # at this point, even though they will match once the right side path makes its
    # turn towards the end.
    #
    # We could consider tracking the number of movements and number of turns separately
    # for each path, then calculate the best cost once we reach the end position. Once
    # this is calculated, we can then cut off any paths that exceed this cost. Maybe
    # this could be extended to say that we should only start cutting off paths once
    # we reach the end position, as we can't be sure that a path is a best path based
    # on its current cost alone.
    #
    # Another idea that we could try is calculating a single best path to the end for
    # a reference, then using this path to determine the other best paths.

    while queue:
        node = heappop(queue)
        cost, _, position, direction, _ = node

        if maze[position.y][position.x] == Cell.WALL:
            continue

        if cost > min_cost_to_position[end_position]:
            continue

        if position in min_cost_to_position and cost > min_cost_to_position[position]:
            continue

        min_cost_to_position[position] = cost
        if position == end_position:
            best_paths.append(node)
            continue

        left_direction = direction.turn_counter_clockwise()
        right_direction = direction.turn_clockwise()

        left_position = left_direction.advance(position)
        forward_position = direction.advance(position)
        right_position = right_direction.advance(position)

        move_forward_cost = cost + move_cost
        move_side_cost = turn_cost + move_forward_cost

        left_step = (
            move_side_cost,
            count(),
            left_position,
            left_direction,
            node,
        )
        forward_step = (
            move_forward_cost,
            count(),
            forward_position,
            direction,
            node,
        )
        right_step = (
            move_side_cost,
            count(),
            right_position,
            right_direction,
            node,
        )

        heappush(queue, left_step)
        heappush(queue, forward_step)
        heappush(queue, right_step)

    print(best_paths)

    best_path_positions = set()
    for end_node in best_paths:
        node = end_node
        while node:
            _, _, position, _, previous = node
            best_path_positions.add(position)
            node = previous

    display_maze = maze.copy()
    for y, row in enumerate(display_maze):
        for x, _ in enumerate(row):
            if Position(x, y) in best_path_positions:
                display_maze[y][x] = "O"

    print_maze(display_maze)

    return len(best_path_positions)


def main() -> None:
    """Read the maze layout from an input file and process it."""

    input_file = TEST_FILE_1
    file_path = path.join(path.dirname(__file__), input_file)

    maze = read_maze(file_path)
    print_maze(maze)

    start_time = perf_counter()
    min_cost = min_cost_to_end(maze)
    end_time = perf_counter()

    print(f"Time: {end_time - start_time:.6f} s")
    print(min_cost)

    start_time = perf_counter()
    best_tile_count = count_best_path_tiles(maze)
    end_time = perf_counter()

    print(f"Time: {end_time - start_time:.6f} s")
    print(best_tile_count)


if __name__ == "__main__":
    main()


"""
def count_best_path_tiles(
    maze: Maze,
    start_direction: Direction = DEFAULT_STARTING_DIRECTION,
    move_cost: int = DEFAULT_MOVE_COST,
    turn_cost: int = DEFAULT_TURN_COST,
) -> int:

    start_position = find_start_position(maze)
    end_position = find_end_position(maze)

    print(start_position)
    print(end_position)

    count = create_counter(0)
    queue = [(0, count(), start_position, start_direction, None)]

    # We use a sentinel value for the end position to simplify best path logic.
    min_cost_to_position = {
        end_position: 999999999,
    }

    best_paths = []

    # Since we're using a variant of Dijkstra's algorithm, we know that the first path
    # to reach the end will be one of the shortest/best paths. This means that we can
    # track the number of tiles visited by this path and then use it to determine which
    # of the remaining paths are also best paths. Any path that exceeds this count can
    # be terminated early, saving time and memory.

    # All the paths will have some crossover so using a set to eliminate duplicates
    # might not be the best idea. One thing we could try is including the previous
    # position for any given node in the queue. With this, we could keep track of the
    # last nodes of each best path and then unwind them to recreate the paths.
    while queue:
        node = heappop(queue)
        cost, _, position, direction, _ = node

        if maze[position.y][position.x] == Cell.WALL:
            continue

        if cost > min_cost_to_position[end_position]:
            continue

        if position in min_cost_to_position and cost > min_cost_to_position[position]:
            continue

        min_cost_to_position[position] = cost
        if position == end_position:
            best_paths.append(node)
            continue

        left_direction = direction.turn_counter_clockwise()
        right_direction = direction.turn_clockwise()

        left_position = left_direction.advance(position)
        forward_position = direction.advance(position)
        right_position = right_direction.advance(position)

        move_forward_cost = cost + move_cost
        move_side_cost = turn_cost + move_forward_cost

        left_step = (
            move_side_cost,
            count(),
            left_position,
            left_direction,
            node,
        )
        forward_step = (
            move_forward_cost,
            count(),
            forward_position,
            direction,
            node,
        )
        right_step = (
            move_side_cost,
            count(),
            right_position,
            right_direction,
            node,
        )

        heappush(queue, left_step)
        heappush(queue, forward_step)
        heappush(queue, right_step)

    print(best_paths)

    best_path_positions = set()
    for end_node in best_paths:
        node = end_node
        while node:
            _, _, position, _, previous = node
            best_path_positions.add(position)
            node = previous

    display_maze = maze.copy()
    for y, row in enumerate(display_maze):
        for x, _ in enumerate(row):
            if Position(x, y) in best_path_positions:
                display_maze[y][x] = "O"

    print_maze(display_maze)

    return len(best_path_positions)

"""
