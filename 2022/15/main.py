import re

import numpy as np

from tools import parse_lines, print_part


def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


@print_part
def solve(filepath: str, part: int = 1):
    all = [
        tuple(map(int, m))
        for line in parse_lines(filepath)
        for m in re.findall(r"x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)", line)
    ]

    all_x = [x for xs_xb in [[coords[0], coords[2]] for coords in all] for x in xs_xb]
    all_y = [y for ys_yb in [[coords[1], coords[3]] for coords in all] for y in ys_yb]
    beacons = [(coords[2], coords[3]) for coords in all]

    distances = [manhattan_distance(*coords) for coords in all]
    max_dist = max(distances)

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    if part == 1:
        min_x -= max_dist
        max_x += max_dist
    else:
        min_x = max(0, min_x)
        max_x = min(4000000, max_x)
        min_y = max(0, min_y)
        max_y = min(4000000, max_y)
    width = max_x - min_x + 1

    coords_dist = [(a, d) for a, d in zip(all, distances)]
    coords_dist.sort(key=lambda x: x[-1])

    if part == 1:
        row_y = 10 if "short" in filepath else 2000000
        row = np.zeros((width,), dtype=int)

        for coord, d in coords_dist:
            cs, rs, cb, rb = coord
            straight_down_distance = manhattan_distance(rs, cs, row_y, cs)
            if d >= straight_down_distance:
                diff = d - straight_down_distance
                col_idxs = [
                    x - min_x
                    for x in range(cs - diff, cs + diff + 1)
                    if min_x <= x <= max_x and (x, row_y) not in beacons
                ]
                row[col_idxs] = 1

        print(sum(row))
    else:
        for row_y in range(max_y):
            print(row_y)
            row = np.zeros((width,), dtype=int)

            for coord, d in coords_dist:
                cs, rs, cb, rb = coord
                straight_down_distance = manhattan_distance(rs, cs, row_y, cs)
                if d >= straight_down_distance:
                    diff = d - straight_down_distance
                    col_idxs = [
                        x - min_x
                        for x in range(cs - diff, cs + diff + 1)
                        if min_x <= x <= max_x
                    ]
                    row[col_idxs] = 1
            print(row)


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
    FILEPATH = "input.txt"
    # solve(FILEPATH, part=1)
