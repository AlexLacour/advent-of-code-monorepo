import copy
from aoc_utils import read_input

input_disk_map = read_input(
    as_type=lambda line: list(map(int, line)), one_line=True, separator=None
)


def parse_memory(disk_map: list[int]) -> list[tuple]:
    # put memory into a readable format
    memory = []
    for disk_name, disk_index in enumerate(range(0, len(disk_map), 2)):
        memory.append((disk_name, sum(disk_map[:disk_index]), disk_map[disk_index]))

    empty_spaces = []
    for disk, next_disk in zip(memory, memory[1:]):
        _, disk_start_index, disk_size = disk
        _, next_disk_start_index, _ = next_disk

        empty_space_size = next_disk_start_index - (disk_start_index + disk_size)

        if empty_space_size:
            empty_spaces.append((None, disk_start_index + disk_size, empty_space_size))

    memory = sorted([*memory, *empty_spaces], key=lambda mem_space: mem_space[1])

    return memory


# script
memory = parse_memory(input_disk_map)


def fix_memory(
    memory_to_fix: list[tuple], with_fragmentation: bool = True
) -> list[tuple]:
    empty_spaces_queue = [m for m in memory_to_fix if m[0] is None]
    while empty_spaces_queue:
        empty_mem_space = empty_spaces_queue.pop(0)
        _, file_position, file_size = empty_mem_space

        # what can fill the space ?
        moved_size = 0
        moved_files = []
        fragmented_files = []

        if with_fragmentation:
            while moved_size < file_size:
                last_file = [file for file in memory_to_fix if file[0] is not None][-1]

                if last_file[1] < file_position:
                    break

                if moved_size + last_file[-1] <= file_size:
                    moved_files.append(last_file)
                else:
                    fragmented_files.append(last_file)
                memory_to_fix.remove(last_file)

                moved_size += last_file[-1]
        else:
            for moved in memory_to_fix[::-1]:
                if (
                    moved[0] is not None
                    and moved_size + moved[-1] <= file_size
                    and moved[1] > file_position
                ):
                    moved_files.append(moved)
                    moved_size += moved[-1]
                    memory_to_fix.remove(moved)

        # start moving
        new_position = file_position
        for moved_id, _, moved_size in moved_files:
            moved = (moved_id, new_position, moved_size)
            memory_to_fix.append(moved)
            new_position += moved_size

        if not with_fragmentation:
            if (
                0
                < (
                    total_moved_size := sum(
                        [moved_size for _, _, moved_size in moved_files]
                    )
                )
                < file_size
            ):
                new_empty_space = (None, new_position, file_size - total_moved_size)
                empty_spaces_queue.append(new_empty_space)

        for frag_id, frag_position, frag_size in fragmented_files:
            size_difference = file_size - sum(
                [moved_file[-1] for moved_file in moved_files]
            )
            moved = (frag_id, new_position, size_difference)
            remaining = (frag_id, frag_position, frag_size - size_difference)

            memory_to_fix.append(moved)
            memory_to_fix.append(remaining)

        memory_to_fix = sorted(memory_to_fix, key=lambda space: space[1])

    return memory_to_fix


def checksum(mem: list[tuple]) -> int:
    checksum = 0
    for file_id, file_position, file_size in mem:
        checksum += (
            file_id * sum(range(file_position, file_position + file_size))
            if file_id is not None
            else 0
        )
    return checksum


fixed_memory = fix_memory(memory_to_fix=copy.deepcopy(memory))
print(f"{checksum(fixed_memory)=}")

fixed_memory = fix_memory(memory_to_fix=copy.deepcopy(memory), with_fragmentation=False)
print(f"{checksum(fixed_memory)=}")
