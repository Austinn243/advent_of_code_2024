"""
Advent of Code, Day 9
Disk Fragmenter
https://adventofcode.com/2024/day/9
"""

from collections import defaultdict
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


class FileBlock(NamedTuple):
    """A file block with its identifier and size."""

    id: int
    size: int


EmptyBlock = int
Block = FileBlock | EmptyBlock


def read_disk_map(file_path: str) -> str:
    """Read the disk map from the input file."""

    with open(file_path, encoding="utf-8") as file:
        return file.read().strip()

    # def parse_blocks(disk_map: str) -> deque[Block]:
    #     """Read the block information from the disk map."""

    #     blocks = deque()
    #     for i, block in enumerate(disk_map):
    #         block_value = int(block)
    #         if i % 2 == 0:
    #             blocks.append(FileBlock(i // 2, block_value))
    #         else:
    #             blocks.append(block_value)

    #     return blocks

    # def compress_using_fragments(blocks: deque[Block]) -> list[int]:
    #     """Compress the disk map by filling gaps with file fragments."""

    #     def write_file(compressed: list[int], identifier: int, size: int) -> None:
    #         for _ in range(size):
    #             compressed.append(identifier)

    #     def move_fragments(
    #         compressed: list[int],
    #         blocks: deque[Block],
    #         remaining_space: int,
    #     ) -> None:
    #         while remaining_space > 0:
    #             next_block = blocks.pop()
    #             match next_block:
    #                 case FileBlock(id, size):
    #                     if size <= remaining_space:
    #                         write_file(compressed, id, size)
    #                         remaining_space -= size
    #                     else:
    #                         write_file(compressed, id, remaining_space)
    #                         blocks.append(FileBlock(id, size - remaining_space))
    #                         remaining_space = 0
    #                 case _:
    #                     continue

    #     compressed = []
    #     while blocks:
    #         block = blocks.popleft()
    #         match block:
    #             case FileBlock(id, size):
    #                 write_file(compressed, id, size)
    #             case EmptyBlock(remaining_space):
    #                 move_fragments(compressed, blocks, remaining_space)

    #     return compressed

    # def compress_using_full_files(blocks: deque[Block]) -> list[int]:
    """Compress the disk map by filling gaps only with files that fit."""

    # If we keep the disk map as is without splitting the blocks, we can
    # determine the following information:
    # - Whether the block is a file or empty space based on whether the index
    # of the block is even or odd. Files have even indices.
    # - The identifier of a file is its index divided by 2.


def compress_using_fragments(disk_map: str) -> list[int]:
    """Compress the disk map by filling gaps with file fragments."""

    blocks = [int(value) for value in disk_map]

    compressed = []
    left_index = 0
    right_index = len(disk_map) - 1

    while left_index <= right_index:
        size = blocks[left_index]
        is_file = left_index % 2 == 0
        if is_file:
            file_id = left_index // 2
            for _ in range(size):
                compressed.append(file_id)
        else:
            remaining_size = size
            while remaining_size > 0:
                file_id = right_index // 2
                file_size = blocks[right_index]

                if file_size <= remaining_size:
                    for _ in range(file_size):
                        compressed.append(file_id)

                    remaining_size -= file_size
                    right_index -= 2
                else:
                    for _ in range(remaining_size):
                        compressed.append(file_id)

                    blocks[right_index] -= remaining_size
                    remaining_size = 0

        left_index += 1

    return compressed


def compress_using_full_files(disk_map: str) -> list[int]:
    """Compress the disk map by filling gaps only with files that fit."""

    blocks = [int(value) for value in disk_map]
    file_ids_by_size = defaultdict(set)

    for i, size in enumerate(blocks):
        is_file = i % 2 == 0
        if is_file:
            file_id = i // 2
            file_ids_by_size[size].add(file_id)

    print(file_ids_by_size)

    compressed = []
    index = 0

    # FIXME: This doesn't account for the spaces added after moving a file of a smaller
    # size than the block. Maybe we should just try to use a two pointer method instead?

    while file_ids_by_size:
        size = blocks[index]
        is_file = index % 2 == 0
        if is_file:
            file_id = index // 2
            for _ in range(size):
                compressed.append(file_id)

            file_ids_by_size[size].remove(file_id)
            if not file_ids_by_size[size]:
                del file_ids_by_size[size]
        else:
            file_id = 0
            file_size = 0
            for possible_size in range(min(file_ids_by_size.keys()), size + 1):
                candidate = max(file_ids_by_size[possible_size])
                if candidate > file_id:
                    file_id = candidate
                    file_size = possible_size

            remaining_size = size - file_size
            for _ in range(file_size):
                compressed.append(file_id)
            for _ in range(remaining_size):
                compressed.append(0)

            if file_size > 1:
                file_ids_by_size[file_size].remove(file_id)
                if not file_ids_by_size[file_size]:
                    del file_ids_by_size[file_size]

        index += 1

    return compressed


def checksum(compressed: list[int]) -> int:
    """Calculate the checksum of the compressed disk map."""

    return sum(identifier * i for i, identifier in enumerate(compressed))


def main() -> None:
    """Read the disk map from the input file and process it."""

    input_file = TEST_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    disk_map = read_disk_map(file_path)

    # blocks = parse_blocks(disk_map)
    # print(parse_blocks)

    # compressed = compress_using_fragments(blocks)
    # print(compressed)
    # print(checksum(compressed))

    print(checksum(compress_using_fragments(disk_map)))
    print(checksum(compress_using_full_files(disk_map)))


if __name__ == "__main__":
    main()
