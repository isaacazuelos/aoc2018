from collections import namedtuple

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

Cart = namedtuple("Cart", ["heading", "direction"])


def next_turn(direction):
    return (direction + 1) % 3


def turn(heading, direction):
    # turning is when we hit and intersection and get to choose a new heading
    if direction == straight:
        return heading
    elif heading == north and direction == left:
        return east
    elif heading == north and direction == right:
        return west
    elif heading == west and direction == left:
        return south
    elif heading == west and direction == right:
        return north
    elif heading == east and direction == left:
        return north
    elif heading == east and direction == right:
        return south
    elif heading == south and direction == left:
        return east
    elif heading == south and direction == right:
        return west
    else:
        raise Exception(f"cannot turn {heading} by {direction}")


def corner(heading, corner):
    # cornering is when we're forced to change heading by the track
    if heading == north and corner == "\\":
        return west
    elif heading == south and corner == "\\":
        return east
    elif heading == east and corner == "\\":
        return south
    elif heading == west and corner == "\\":
        return north
    elif heading == north and corner == "/":
        return east
    elif heading == south and corner == "/":
        return west
    elif heading == east and corner == "/":
        return north
    elif heading == west and corner == "/":
        return south
    else:
        raise Exception(f"cannot corner on {corner} heading {heading} ")


def move_by(pos, heading):
    (x, y) = pos
    if heading == north:
        return (x, y - 1)
    elif heading == south:
        return (x, y + 1)
    elif heading == east:
        return (x + 1, y)
    elif heading == west:
        return (x - 1, y)
    elif heading == crash:
        return pos
    else:
        raise Exception(f"cannot move {pos} in {heading}")


def tick(grid, carts):
    new = {}

    # `for cart in carts` is out of order
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) not in carts:
                continue

            pos = (x, y)
            cart = carts[pos]

            new_pos = move_by(pos, cart.heading)
            (nx, ny) = new_pos

            on_tile = grid[ny][nx]

            # determine new heading
            if on_tile == "+":
                new_heading = turn(cart.heading, cart.direction)
                new_direction = next_turn(cart.direction)
            elif on_tile == "/" or on_tile == "\\":
                new_heading = corner(cart.heading, on_tile)
                new_direction = cart.direction
            else:
                new_heading = cart.heading
                new_direction = cart.direction

            # detect crash
            if new_pos in new:
                new_heading = crash

            new[new_pos] = Cart(heading=new_heading, direction=new_direction)

    return new


def print_gird(grid, carts):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in carts:
                cart = carts[(x, y)]
                print(cart.heading, end="")
            else:
                print(grid[y][x], end="")
        print()


def has_crash(carts):
    for pos, cart in carts.items():
        if cart.heading == crash:
            return pos


def part_1(grid, carts):
    states = [carts]
    tock = 0
    while not has_crash(carts):
        carts = tick(grid, carts)
        states.append(carts)
        tock += 1

    print(tock)
    print_gird(grid, states[-2])
    print_gird(grid, states[-1])
    (x, y) = has_crash(carts)
    print(f"part 1: {x},{y}")


def part_2():
    print("part 2:")


lines = open("input.txt", "r").read().split("\n")

# notice that the only characters that matter are "/ \ + v ^ < >" We can
# ignore | and -  as the carts are moving in that direction already.
#
# Also notice that the grid is [y][x] :(
grid = list(map(list, lines))

carts = {}
for y in range(len(grid)):
    for x in range(len(grid[y])):
        char = grid[y][x]
        if char in [north, south, east, west]:
            carts[(x, y)] = Cart(heading=char, direction=left)
            if char in "<>":
                grid[y][x] = "-"
            else:
                grid[y][x] = "|"

part_1(grid, carts)
