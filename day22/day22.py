from collections import deque

# problem
DEPTH = 11109
TARGET = (9, 731)

# example
# DEPTH = 510
# TARGET = (10, 10)

ROCKY = 0
WET = 1
NARROW = 2

known_gidx = {(0, 0): 0, TARGET: 0}


def gidx(pos):
    if pos in known_gidx:
        return known_gidx[pos]
    elif pos[1] == 0:
        idx = pos[0] * 16807
    elif pos[0] == 0:
        idx = pos[1] * 48271
    else:
        (x, y) = pos
        idx = erosion((x - 1, y)) * erosion((x, y - 1))

    known_gidx[pos] = idx
    return idx


def erosion(pos):
    return (gidx(pos) + DEPTH) % 20183


def region_type(pos):
    return erosion(pos) % 3


def risk_level(top_left=(0, 0), bottom_right=TARGET):
    risk = 0
    for x in range(top_left[0], bottom_right[0] + 1):
        for y in range(top_left[1], bottom_right[1] + 1):
            risk += region_type((x, y))
    return risk


def print_grid():
    for y in range(TARGET[0] + 1):
        for x in range(TARGET[1] + 1):
            ty = region_type((x, y))
            if ty == ROCKY:
                c = "."
            elif ty == WET:
                c = "="
            else:
                c = "|"
            print(c, end="")
        print("")


def part_1():
    print("part 1:", risk_level())


part_1()
