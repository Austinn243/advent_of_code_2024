"""
Advent of Code 2024: Day 2
Red-Nosed Reports
https://adventofcode.com/2024/day/2
"""

from collections.abc import Callable, Iterable
from itertools import pairwise
from os import path

INPUT_FILE = "input.txt"
MIN_LEVEL_DIFFERENCE = 1
MAX_LEVEL_DIFFERENCE = 3

Report = list[int]


def partition[T](
    predicate: Callable[[T], bool],
    iterable: Iterable[T],
) -> tuple[list[T], list[T]]:
    """Partition an iterable into two lists based on a predicate."""

    true_list, false_list = [], []

    for item in iterable:
        if predicate(item):
            true_list.append(item)
        else:
            false_list.append(item)

    return true_list, false_list


def read_inputs(file_path: str) -> list[Report]:
    """Read the reports from the input file."""

    with open(file_path, encoding="utf-8") as file:
        return [list(map(int, line.strip().split())) for line in file]


def is_safe_report(
    report: Report,
    min_level_difference: int = MIN_LEVEL_DIFFERENCE,
    max_level_difference: int = MAX_LEVEL_DIFFERENCE,
) -> bool:
    """Check if the report is safe to use.

    A safe report is one where all values are in strictly increasing or strictly
    decreasing order, and the difference between each pair of values is between
    the minimum and maximum level differences.
    """

    differences = [num2 - num1 for num1, num2 in pairwise(report)]

    all_safe_changes = all(
        min_level_difference <= abs(diff) <= max_level_difference
        for diff in differences
    )
    all_strictly_increasing = all(diff > 0 for diff in differences)
    all_strictly_decreasing = all(diff < 0 for diff in differences)

    return all_safe_changes and (all_strictly_increasing or all_strictly_decreasing)


def is_relatively_safe_report(
    report: Report,
    min_level_difference: int = MIN_LEVEL_DIFFERENCE,
    max_level_difference: int = MAX_LEVEL_DIFFERENCE,
) -> bool:
    """Determine if the report is relatively safe to use.

    A relatively safe report is one where there is at most one exception to the
    safe report conditions.
    """

    return any(
        is_safe_report(
            report[:i] + report[i + 1 :],
            min_level_difference,
            max_level_difference,
        )
        for i in range(len(report))
    )


def main() -> None:
    """Read reports from a file and determine how many are safe or relatively safe."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    reports = read_inputs(file_path)

    safe_reports, unsafe_reports = partition(is_safe_report, reports)
    safe_report_count = len(safe_reports)
    print(safe_report_count)

    relatively_safe_reports = [
        report for report in unsafe_reports if is_relatively_safe_report(report)
    ]
    relatively_safe_report_count = len(relatively_safe_reports)
    print(relatively_safe_report_count)

    total_safe_reports = safe_report_count + relatively_safe_report_count
    print(total_safe_reports)


if __name__ == "__main__":
    main()
