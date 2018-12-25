import heapq
from collections import deque, defaultdict

START = (0, 0)

# problem
# DEPTH = 11109
# TARGET = (9, 731)

# example
DEPTH = 510
TARGET = (10, 10)

ROCKY = 0
WET = 1
NARROW = 2

NEITHER_TOOL = "n"
TORCH = "t"
CLIMBING_GEAR = "c"
TOOLS = "ntc"

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


def fastest_time():
    wavefront = set((START, tool) for tool in TOOLS)
    distances = defaultdict(lambda: 2 ** 64)
    previous = {}

    while TARGET not in distances:
        # TODO: use a priority queue instead
        shortest_path = min(wavefront, key=lambda w: distances[w[0]])
        node = wavefront.remove(shortest_path)
        for cursor in adj(node):
            # TODO do it.


    return rebuild(distances, previous)


def rebuild(dist, prev):
    s = []
    u = TARGET
    if u in prev or u == (0, 0):
        while u in prev:
            s.append((u, dist[u]))
            u = prev[u]

    s.reverse()
    return s


def cost_to_move(u, v):
    return 1


def adj(pos):
    (x, y) = pos[0]  # pos is ((x, y), tool)
    aa = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for a in aa:
        if a[0] >= 0 and a[1] >= 0:
            for tool in [NEITHER_TOOL, TORCH, CLIMBING_GEAR]:
                yield (a, tool)


def part_2():
    path = fastest_time()
    print("part 2:")
    print(path)
    print(sum(map(lambda x: x[0], path)))


part_1()
part_2()
