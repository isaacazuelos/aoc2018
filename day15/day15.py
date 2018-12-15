import sys


def adjacent_to(position):
    (x, y) = position
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                # positions are not self-adjacent
                continue
            else:
                yield (x + dx, y + dy)


def reachable(start, grid, guys):
    # holy shit, this isn't trivial at all.
    r = set()

    working = set()
    working.add(start)

    while working:
        # print("working set is size", len(working))
        pos = working.pop()
        for adj in adjacent_to(pos):
            (x, y) = adj
            if (grid[y][x] == ".") and not (guy_at(adj, guys)) and adj not in r:
                working.add(adj)

        r.add(pos)

    r.remove(start)
    return r


def distance(a, b):
    (ax, ay) = a
    (bx, by) = b
    return abs(ax - bx) + abs(ay - by)


def reading_order_key(point):
    (x, y) = point
    return (y, x)


class Guy:
    def __init__(self, position, grid, guys, hp=200, atk=3, bad=False):
        self.bad = bad
        self.position = position
        self.hp = hp
        self.atk = atk

        self.grid = grid
        self.guys = guys

    def glyph(self):
        if self.bad:
            return "G"
        else:
            return "E"

    def reading_order_key(self):
        (x, y) = self.position
        return (y, x)

    def act(self):
        attackable = self.enemies_in_range()
        if attackable:
            target = attackable.pop()
            self.attack(target)
            return

        in_range = set()
        for target in self.pick_targets():
            open_pos = target.open_adjacent()
            in_range.update(open_pos)
        in_range = list(sorted(in_range, key=reading_order_key))

        if in_range:
            self.move(in_range)
            return

    def move(self, in_range):
        r = reachable(self.position, self.grid, self.guys)

        distance_from_self = lambda square: distance(square, self.position)

        for position in sorted(in_range, key=distance_from_self):
            # closest first
            if position in r:
                self.step_towards(position)
                return

    def step_towards(self, position):
        for landing in self.open_adjacent():
            if distance(landing, position) < distance(self.position, position):
                self.position = landing
                return

    def attack(self, target):
        pass

    def enemies_in_range(self):
        res = []
        for adj_pos in self.adjacent_positions():
            guy = guy_at(adj_pos, self.guys)
            if guy and self.is_enemy(guy):
                res.append(guy)
        return res

    def is_enemy(self, target):
        return self.bad != target.bad

    def pick_targets(self):
        targets = []
        for guy in sorted_guys(self.guys):
            if self.is_enemy(guy):
                targets.append(guy)

        targets.sort(key=Guy.reading_order_key)

        return targets

    def open_adjacent(self):
        okay = []

        # in reading order
        for (nx, ny) in self.adjacent_positions():
            if (self.grid[ny][nx] == ".") and (not guy_at((nx, ny), self.guys)):
                okay.append((nx, ny))

        okay.sort(key=reading_order_key)

        return okay

    def adjacent_positions(self):
        (x, y) = self.position
        for (dx, dy) in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            yield (x + dx, y + dy)


def point_in_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            yield (x, y)


# in reading order
def sorted_guys(guys):
    return sorted(guys, key=lambda g: (g.position[1], g.position[0]))


def guy_at(pos, guys):
    for guy in guys:
        if guy.position == pos:
            return guy


def extract_guys(grid):
    guys = set()
    for (x, y) in point_in_grid(grid):
        tile = grid[y][x]
        if tile in "EG":
            guy = Guy((x, y), grid, guys, bad=(tile == "G"))
            guys.add(guy)
            grid[y][x] = "."
    return guys


def print_grid(grid, guys=None):
    guys = guys or set()
    for (x, y) in point_in_grid(grid):
        if x == 0:
            print()

        if guy_at((x, y), guys):
            cart = guy_at((x, y), guys)
            print(cart.glyph(), end="")
        else:
            print(grid[y][x], end="")

    print()


def tick(grid, guys):
    for guy in sorted_guys(guys):
        print("moving guy at:", guy.position)
        guy.act()


def simulate(grid, guys, end=None):
    i = 0

    while any(guy.pick_targets() for guy in guys) and ((not end) or i < end):
        print("turn", i)
        for guy in sorted_guys(guys):
            guy.act()

            print_grid(grid, guys)
            print()
            # tick(grid, guys)
        i += 1

    print("turn", i)
    print_grid(grid, guys)


lines = open(sys.argv[1], "r").read().split("\n")

grid = list(map(list, lines))


guys = extract_guys(grid)

if len(sys.argv) == 3:
    end = int(sys.argv[2])
else:
    end = None


simulate(grid, guys, end=end)
