"""
Advent of Code 2024, Day 12
Garden Groups
https://adventofcode.com/2024/day/12
"""

from collections import Counter, defaultdict
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"
TEST_FILE_3 = "test3.txt"


class Position(NamedTuple):
    """Represents a position in the garden map."""

    x: int
    y: int


class Edge(NamedTuple):
    """Represents the edge of a position in the garden map.

    Edges are undirected, so two edges are considered equal if they connect the same
    positions.
    """

    start: Position
    end: Position

    def __eq__(self, value: "Edge") -> bool:
        """Check if two edges are equal."""

        return (self.start == value.start and self.end == value.end) or (
            self.start == value.end and self.end == value.start
        )

    def __hash__(self):
        """Calculate the hash of the edge."""

        return hash((self.start.x + self.end.x, self.start.y + self.end.y))


GardenMap = list[str]
RegionID = int
Region = set[Position]


def read_garden_map(file_path: str) -> GardenMap:
    """Read the garden map from the file."""

    with open(file_path, encoding="utf-8") as file:
        return file.read().splitlines()


def neighbors(position: Position, garden_map: GardenMap) -> list[Position]:
    """Find all neighbors of the given position."""

    neighbors = [
        Position(position.x - 1, position.y),
        Position(position.x + 1, position.y),
        Position(position.x, position.y - 1),
        Position(position.x, position.y + 1),
    ]

    return [
        neighbor for neighbor in neighbors if is_valid_position(neighbor, garden_map)
    ]


def is_valid_position(position: Position, garden_map: GardenMap) -> bool:
    """Check if the position is valid in the garden map."""

    return 0 <= position.y < len(garden_map) and 0 <= position.x < len(garden_map[0])


def find_regions(garden_map: GardenMap) -> dict[RegionID, list[Region]]:
    """Find all regions in the garden map grouped by their plant type."""

    regions = defaultdict(list)
    visited = set()

    for y, row in enumerate(garden_map):
        for x, plant_type in enumerate(row):
            position = Position(x, y)
            if position in visited:
                continue

            region = set()
            stack = [position]

            while stack:
                current = stack.pop()

                visited.add(current)
                region.add(current)

                region_neighbors = [
                    neighbor
                    for neighbor in neighbors(current, garden_map)
                    if neighbor not in visited
                    and garden_map[neighbor.y][neighbor.x] == plant_type
                ]

                for neighbor in region_neighbors:
                    stack.append(neighbor)

            regions[plant_type].append(region)

    return regions


def area(region: Region) -> int:
    """Calculate the area of the region."""

    return len(region)


def edges(region: Region) -> set[Edge]:
    """Find all edges of the region."""

    edge_counts = Counter()

    for x, y in region:
        top_left = Position(x, y)
        top_right = Position(x + 1, y)
        bottom_left = Position(x, y + 1)
        bottom_right = Position(x + 1, y + 1)

        edges = [
            Edge(top_left, top_right),
            Edge(top_right, bottom_right),
            Edge(bottom_right, bottom_left),
            Edge(bottom_left, top_left),
        ]

        for edge in edges:
            edge_counts[edge] += 1

    return {edge for edge, count in edge_counts.items() if count == 1}


def perimeter(region: Region) -> int:
    """Calculate the perimeter of the region."""

    return len(edges(region))


def price(region: Region) -> int:
    """Calculate the price of the region."""

    return area(region) * perimeter(region)


def side_count(region: Region) -> int:
    """Count the number of sides of the region."""

    region_edges = edges(region)

    edge_ends_by_start_position: dict[Position, Position] = {}
    for edge in region_edges:
        edge_ends_by_start_position[edge.start] = edge.end

    side_count = 0
    for first, second in region_edges:
        third = edge_ends_by_start_position[second]

        x_offset = abs(first.x - third.x)
        y_offset = abs(first.y - third.y)

        edges_make_corner = x_offset == 1 and y_offset == 1
        if edges_make_corner:
            side_count += 1

    return side_count


def discounted_price(region: Region) -> int:
    """Calculate the discounted price of the region."""

    return area(region) * side_count(region)


def main() -> None:
    """Read the garden map from an input file and process its groups."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    garden_map = read_garden_map(file_path)

    regions = find_regions(garden_map)

    standard_total_price = sum(
        price(region) for plant_regions in regions.values() for region in plant_regions
    )
    print(f"The standard fencing price is {standard_total_price}")

    discounted_total_price = sum(
        discounted_price(region)
        for plant_regions in regions.values()
        for region in plant_regions
    )
    print(f"The discounted fencing price is {discounted_total_price}")


if __name__ == "__main__":
    main()
