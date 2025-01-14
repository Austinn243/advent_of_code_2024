"""
Advent of Code 2024, Day 23
LAN Party
https://adventofcode.com/2024/day/23
"""

from collections import defaultdict
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


Connection = tuple[str, str]
Graph = dict[str, set[str]]


def read_connections(file_path: str) -> list[Connection]:
    """Read connections from a file."""

    connections = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            computer1, computer2 = line.strip().split("-")
            connections.append((computer1, computer2))

    return connections


def create_graph(connections: list[Connection]) -> Graph:
    """Create a graph of computer connections."""

    graph = defaultdict(set)

    for computer1, computer2 in connections:
        graph[computer1].add(computer2)
        graph[computer2].add(computer1)

    return graph


def find_threesomes_containing_t_prefix_computer(graph: Graph) -> set[frozenset[str]]:
    """Find all combinations of three connected computers containing a computer starting with 't'."""

    computers_with_t_prefix = {
        computer for computer in graph.keys() if computer.startswith("t")
    }
    print(computers_with_t_prefix)

    threesomes = set()

    for computer in computers_with_t_prefix:
        for second in graph[computer]:
            for third in graph[second]:
                if third in graph[computer]:
                    threesomes.add(frozenset([computer, second, third]))

    return threesomes


def find_largest_connected_group(graph: Graph) -> set[str]:
    """Find the computers in the largest connected group."""

    groups = set()

    def bron_kerbosch(
        clique: set[str],
        candidates: set[str],
        excluded: set[str],
    ) -> None:
        if not candidates and not excluded:
            groups.add(frozenset(clique))
            return

        pivot = set.union(candidates, excluded).pop()

        for vertex in set.difference(candidates, graph[pivot]):
            bron_kerbosch(
                set.union(clique, {vertex}),
                set.intersection(candidates, graph[vertex]),
                set.intersection(excluded, graph[vertex]),
            )

            candidates.discard(vertex)
            excluded.add(vertex)

    bron_kerbosch(set(), set(graph.keys()), set())
    return max(groups, key=len)


def find_password(graph: Graph) -> str:
    """Find the password for the LAN party."""

    computers = find_largest_connected_group(graph)
    print(computers)

    return ",".join(sorted(computers))


def main() -> None:
    """Read commputer connections from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    connections = read_connections(file_path)

    graph = create_graph(connections)

    threesomes_with_t = find_threesomes_containing_t_prefix_computer(graph)
    print(len(threesomes_with_t))

    password = find_password(graph)
    print(password)


if __name__ == "__main__":
    main()
