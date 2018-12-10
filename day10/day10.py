from collections import defaultdict

# Point = namedtuple("Point", ["x", "y", "dx", "dy"])

# from day 6
def points_in_grid(w, h):
    for y in range(h):
        for x in range(w):
            yield (x, y)


def parse_point(line):
    x = int(line[10:16])
    y = int(line[18:24])
    dx = int(line[36:38])
    dy = int(line[40:42])
    return ((x, y), (dx, dy))


def update_points(points):
    gen = defaultdict(set)
    for ((x, y), deltas) in points.items():
        for (dx, dy) in deltas:
            pos = (x + dx, y + dy)
            gen[pos].add((dx, dy))
    return gen


def print_grid(points):
    w = max(x for (x, y) in points.keys())
    h = max(y for (x, y) in points.keys())

    for y in range(0, h):
        for x in range(0, w):
            if points[(x, y)]:
                char = "*"
            else:
                char = "."
            print(char, sep="", end="")
        print()
    print()


def n_points_align(n, points):
    candidates = set(points.keys())
    while candidates:
        (x, y) = candidates.pop()
        if all(points[(x + i, y)] for i in range(n)):
            return True
        if all(points[(x, y + i)] for i in range(n)):
            return True
    return False


def part_1(points, max_gen=11000):
    gens = []
    for gen in range(max_gen):
        if n_points_align(4, points):
            gens.append((gen, points))
        points = update_points(points)
        if not gen % 10 ** 3:
            print("gen", gen)
    return gens


lines = open("input.txt", "r").read().split("\n")

# points: {(x, y): set((dx, dy))}
points = defaultdict(set)
for line in lines:
    (p, v) = parse_point(line)
    points[p].add(v)

part_1_maybe = part_1(points)

for (gen, points) in part_1_maybe:
    print(f"part 1: found answer on gen {gen},")
    print(print_grid(points))
