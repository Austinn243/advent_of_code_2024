"""
Advent of Code 2024, Day 5
Print Queue
https://adventofcode.com/2024/day/5
"""

from collections import defaultdict, namedtuple
from collections.abc import Callable, Iterable
from os import path

INPUT_FILE = "input.txt"
PAGE_NUMBER_SEPARATOR = ","
RULE_SEPARATOR = "|"

DependencyGraph = dict[int, set[int]]
OrderingRule = namedtuple("OrderingRule", ["dependency", "dependent"])
PageUpdate = list[int]


def partition[T](
    predicate: Callable[[T], bool],
    iterable: Iterable[T],
) -> tuple[list[T], list[T]]:
    """Partition an iterable into two lists based on a predicate."""

    left, right = [], []
    for item in iterable:
        if predicate(item):
            left.append(item)
        else:
            right.append(item)

    return left, right


def read_inputs(file_path: str) -> tuple[list[OrderingRule], list[PageUpdate]]:
    """Read the ordering rules and page numbers from an input file."""

    ordering_rules = []
    page_numbers = []

    with open(file_path, encoding="utf-8") as file:
        lines = iter(file.readlines())
        while (line := next(lines).strip()) != "":
            left, right = line.split(RULE_SEPARATOR)
            ordering_rules.append(OrderingRule(int(left), int(right)))

        for line in lines:
            numbers = line.strip().split(PAGE_NUMBER_SEPARATOR)
            page_numbers.append([int(number) for number in numbers])

    return ordering_rules, page_numbers


def is_correctly_ordered(
    page_update: PageUpdate,
    dependencies: DependencyGraph,
) -> bool:
    """Determine if a page update is correctly ordered.

    This is based on the prerequisite ordering rules provided for each page number.
    """

    for i, page_number in enumerate(page_update):
        remaining_pages = page_update[i + 1 :]
        if any(value in dependencies[page_number] for value in remaining_pages):
            return False

    return True


def sum_middle_values(page_updates: list[PageUpdate]) -> int:
    """Add the middle values of each sequence of page numbers."""

    return sum(page_update[len(page_update) // 2] for page_update in page_updates)


def correct_update(
    page_update: PageUpdate,
    dependencies: DependencyGraph,
) -> PageUpdate:
    """Correct the ordering of a page update based on the prerequisites."""

    page_numbers = set(page_update)
    remaining_dependencies = {
        page: dependencies[page] & page_numbers for page in page_update
    }
    corrected_update = []

    while remaining_dependencies:
        current_page = next(
            page
            for page, dependencies in remaining_dependencies.items()
            if not dependencies
        )

        corrected_update.append(current_page)
        remaining_dependencies.pop(current_page)

        for page_dependencies in remaining_dependencies.values():
            page_dependencies.discard(current_page)

    return corrected_update


def main() -> None:
    """Read ordering rules and page numbers from an input file and process them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    ordering_rules, page_updates = read_inputs(file_path)

    dependencies = defaultdict(set)
    for rule in ordering_rules:
        dependencies[rule.dependent].add(rule.dependency)

    correct_updates, incorrect_updates = partition(
        lambda page_update: is_correctly_ordered(page_update, dependencies),
        page_updates,
    )
    print(sum_middle_values(correct_updates))

    corrected_updates = [
        correct_update(page_update, dependencies) for page_update in incorrect_updates
    ]
    print(sum_middle_values(corrected_updates))


if __name__ == "__main__":
    main()
