import sys
from copy import copy
from collections import namedtuple, defaultdict
from itertools import repeat

spring_pos = (500, 0)
clay = "#"
sand = "."

Horz = namedtuple("Horz", ["x", "y"])
Vert = namedtuple("Vert", ["x", "y"])


def is_vert(c):
    return isinstance(c, Vert)


def is_horz(c):
    return isinstance(c, Horz)


def parse_line(line):
    # y=1445, x=423..441
    # x=427, y=1160..1169
    (l, r) = line.split(", ")
    l = int(l[2:])
    (r1, r2) = r.split("..")
    r = (int(r1[2:]), int(r2))
    if line[0] == "x":
        return Vert(x=l, y=r)
    else:
        return Horz(x=r, y=l)


def str_grid(grid):
    res = ""

    min_x = min(point[0] for point in grid)

    for point in point_in_grid(grid):
        if point[0] == 0:
            res += "\n"
        if point[0] >= min_x - 2:  # a nice buffer
            res += grid[point]
    return res


# sue me

WIDTH = None


def width(grid):
    global WIDTH
    if not WIDTH:
        WIDTH = max(grid, key=lambda p: p[0])[0] + 1
    return WIDTH


HEIGHT = None


def height(grid):
    global HEIGHT
    if not HEIGHT:
        HEIGHT = max(grid, key=lambda p: p[1])[1] + 1
    return HEIGHT


def point_in_grid(grid):
    h = height(grid)
    w = width(grid)
    # mw = min(grid, key=lambda p: p[0])[0] - 1

    for y in range(h):
        for x in range(w):
            yield (x, y)


def make_grid(coords):
    width = -1
    height = -1
    for coord in coords:
        if is_horz(coord):
            mx = coord.x[1]
            my = coord.y
        else:
            mx = coord.x
            my = coord.y[1]
        if mx > width:
            width = mx
        if my > height:
            height = my

    grid = defaultdict(lambda: ".")

    for coord in coords:
        if is_horz(coord):
            for x in range(coord.x[0], coord.x[1] + 1):
                grid[(x, coord.y)] = clay
        else:
            for y in range(coord.y[0], coord.y[1] + 1):
                grid[(coord.x, y)] = clay

    grid[spring_pos] = "+"

    return grid


def at(grid, pos):
    return grid[pos]


def below(grid, pos):
    (x, y) = pos
    y += 1
    return grid[(x, y)]


def above(grid, pos):
    (x, y) = pos
    y -= 1
    return grid[(x, y)]


def right(grid, pos):
    (x, y) = pos
    x += 1
    return grid[(x, y)]


def left(grid, pos):
    (x, y) = pos
    x -= 1
    return grid[(x, y)]


def find_span(grid, pos):
    # the range to the left and right until we either
    # have sand below, or clay to the side.

    closed = True
    (x, y) = pos
    l, r = x, x

    while l > 0:
        if below(grid, (l, y)) in "|.":
            closed = False
            break
        elif left(grid, (l, y)) == clay:
            break
        else:
            l -= 1

    while r < width(grid):
        if below(grid, (r, y)) in "|.":
            closed = False
            break
        elif right(grid, (r, y)) == clay:
            break
        else:
            r += 1

    span = (range(l, r + 1), closed)
    return span


def fill(grid, pos):
    if below(grid, pos) in "~#":
        span, closed = find_span(grid, pos)
        tile = "|"
        if closed:
            tile = "~"
        for sx in span:
            grid[(sx, pos[1])] = tile
    elif at(grid, pos) == ".":
        grid[pos] = "|"


def tick(grid):
    new_grid = copy(grid)
    for pos in list(new_grid):
        if at(new_grid, pos) in "+|" and below(new_grid, pos) in ".+|":
            (x, y) = pos
            below_pos = (x, y + 1)
            fill(new_grid, below_pos)

    return new_grid


def trim(grid, max_height):
    for pos in list(grid.keys()):
        if pos[1] >= max_height:
            del grid[pos]


def count(grid, tiles):
    c = 0
    for point in point_in_grid(grid):
        if grid[point] in tiles:
            c += 1
    return c


def part_1(grid):
    # this is just another "stable state" of a cellular automata.

    max_height = height(grid)
    gen = 0

    while True:
        new_grid = tick(grid)
        trim(new_grid, max_height)

        if new_grid == grid:
            break
        else:
            grid = new_grid

        if (gen % 100) == 0:
            print("gen:", gen)
        gen += 1

    open("out.txt", "w").write(str_grid(grid))

    print("part 1:", count(grid, "|~"))


lines = open(sys.argv[1], "r").read().split("\n")

coords = [parse_line(l) for l in lines]

grid = make_grid(coords)

# open("grid.txt", "w").write(str_grid(grid))

part_1(grid)
