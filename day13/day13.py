import sys

from itertools import product

# 'direction' is one of these relative directions
left = 0
straight = 1
right = 2

# There's got to be a clever encoding that makes this math.
# 'heading' is one of these absolute directions, or crash
north = "^"
south = "v"
east = ">"
west = "<"
crash = "X"


class Cart:
    def __init__(self, heading, position, turn_direction=left):
        self.heading = heading
        self.position = position
        self.turn_direction = turn_direction

    def move(self):
        (x, y) = self.position
        if self.heading == north:
            self.position = (x, y - 1)
        elif self.heading == south:
            self.position = (x, y + 1)
        elif self.heading == east:
            self.position = (x + 1, y)
        elif self.heading == west:
            self.position = (x - 1, y)

    def increment_turn_direction(self):
        self.turn_direction = (self.turn_direction + 1) % 3

    def turn(self):
        if self.turn_direction == straight:
            pass
        elif self.heading == north and self.turn_direction == left:
            self.heading = west
        elif self.heading == north and self.turn_direction == right:
            self.heading = east
        elif self.heading == west and self.turn_direction == left:
            self.heading = south
        elif self.heading == west and self.turn_direction == right:
            self.heading = north
        elif self.heading == east and self.turn_direction == left:
            self.heading = north
        elif self.heading == east and self.turn_direction == right:
            self.heading = south
        elif self.heading == south and self.turn_direction == left:
            self.heading = east
        elif self.heading == south and self.turn_direction == right:
            self.heading = west

        self.increment_turn_direction()

    def corner(self, corner):
        # cornering is when we're forced to change heading by the track
        if self.heading == north and corner == "\\":
            self.heading = west
        elif self.heading == south and corner == "\\":
            self.heading = east
        elif self.heading == east and corner == "\\":
            self.heading = south
        elif self.heading == west and corner == "\\":
            self.heading = north
        elif self.heading == north and corner == "/":
            self.heading = east
        elif self.heading == south and corner == "/":
            self.heading = west
        elif self.heading == east and corner == "/":
            self.heading = north
        elif self.heading == west and corner == "/":
            self.heading = south


def cart_at(pos, carts):
    for cart in carts:
        if cart.position == pos:
            return cart


def print_grid(grid, carts=None, crashes=None):
    carts = carts or set()
    crashes = crashes or set()
    for (x, y) in point_in_grid(grid):
        if x == 0:
            print()

        if cart_at((x, y), carts):
            cart = cart_at((x, y), carts)
            print(cart.heading, end="")
        elif cart_at((x, y), crashes):
            cart = cart_at((x, y), crashes)
            print(cart.heading, end="")
        else:
            print(grid[y][x], end="")


def point_in_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            yield (x, y)


def extract_carts(grid):
    carts = set()
    for (x, y) in point_in_grid(grid):
        tile = grid[y][x]
        if grid[y][x] in "><":
            carts.add(Cart(heading=tile, position=(x, y)))
            grid[y][x] = "-"
        elif grid[y][x] in "^v":
            carts.add(Cart(heading=tile, position=(x, y)))
            grid[y][x] = "|"

    return carts


def sorted_carts(carts):
    return list(sorted(carts, key=lambda c: (c.position[1], c.position[0])))


def first_crash(carts):
    for cart in sorted_carts(carts):
        if cart.heading == crash:
            return cart


def remove_crashes(carts, crashes):
    for (l, r) in product(carts, carts):
        if l is r:
            continue
        elif l.position == r.position:
            crashes.add(l)
            crashes.add(r)
            l.heading = crash
            r.heading = crash

    for c in crashes:
        if c in carts:
            carts.remove(c)


def tick(grid, carts, crashes):
    for cart in sorted_carts(carts):

        if cart not in carts:
            continue

        cart.move()

        (nx, ny) = cart.position
        tile = grid[ny][nx]

        if tile in "/\\":
            cart.corner(tile)
        elif tile == "+":
            cart.turn()

        remove_crashes(carts, crashes)


def part_1(grid, carts):
    crashes = set()

    while not crashes:
        tick(grid, carts, crashes)

    print(f"part 1: {crashes.pop().position}")


def part_2(grid, carts):

    while len(carts) > 1:
        crashes = set()
        tick(grid, carts, crashes)

    print(f"part 2: {carts.pop().position}")


lines = open(sys.argv[1], "r").read().split("\n")

grid = list(map(list, lines))

carts = extract_carts(grid)

part_1(grid, carts)
part_2(grid, carts)
