import sys
from collections import defaultdict

# repurposed code from day 15
class Grid:
    EMPTY_TILE = "."
    LUMBER = "#"
    TREE = "|"

    def __init__(self, string=None):
        self.tiles = []
        if string:
            self.load_from_string(string)

    def __eq__(self, rhs):
        for point in self.points():
            if self[point] != rhs[point]:
                return False

        return True

    def clone(self):
        new = Grid()

        new.tiles = [row[:] for row in self.tiles]

        return new

    def points(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                yield (x, y)

    def load_from_string(self, string):
        self.tiles = list(map(list, string.split("\n")))

    def __str__(self):
        res = []
        for pos in self.points():
            if pos[0] == 0:
                res.append("\n")

            tile = self[pos]
            res.append(tile)

        return "".join(res)

    def __getitem__(self, pos):
        (x, y) = pos
        return self.tiles[y][x]

    def __setitem__(self, pos, val):
        (x, y) = pos
        self.tiles[y][x] = val

    @staticmethod
    def adjacent_to(position):
        (x, y) = position
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                # positions are not self-adjacent
                if dx != 0 or dy != 0:
                    yield (x + dx, y + dy)

    def adjacent_on_grid(self, pos):
        for pos in Grid.adjacent_to(pos):
            (x, y) = pos
            if (
                (y >= 0)
                and (y < len(self.tiles))
                and (x < len(self.tiles[y]))
                and (x >= 0)
            ):
                yield pos

    def adjacent_tiles(self, pos):
        for pos in self.adjacent_on_grid(pos):
            yield self[pos]


def next_state(grid, pos):
    if grid[pos] == Grid.EMPTY_TILE:
        # three or more adj trees => trees
        adj_tree_count = sum(map(lambda x: x == Grid.TREE, grid.adjacent_tiles(pos)))
        if adj_tree_count >= 3:
            return Grid.TREE
        else:
            return Grid.EMPTY_TILE
    elif grid[pos] == Grid.TREE:
        # three or more adj trees => lumbar
        adj_lumber_count = sum(
            map(lambda x: x == Grid.LUMBER, grid.adjacent_tiles(pos))
        )
        if adj_lumber_count >= 3:
            return Grid.LUMBER
        else:
            return Grid.TREE
    else:
        adj_lumber_count = sum(
            map(lambda x: x == Grid.LUMBER, grid.adjacent_tiles(pos))
        )
        adj_tree_count = sum(map(lambda x: x == Grid.TREE, grid.adjacent_tiles(pos)))
        if adj_lumber_count and adj_tree_count:
            return Grid.LUMBER
        else:
            return Grid.EMPTY_TILE
        # adjacent to at least one lumbar and at least one trees => remain
        # else => open


def tick(grid):
    next_gen = grid.clone()

    for pos in grid.points():
        next_gen[pos] = next_state(grid, pos)

    return next_gen


def simulate(grid, end=None, print_turns=False):
    i = 0

    while (not end) or i <= end:
        if print_turns:
            print("turn:", i)
            print(grid)

        grid = tick(grid)
        i += 1

    if print_turns:
        print("turn:", i)
        print(grid)

    return grid


def value(grid):
    tree = 0
    lumber = 0
    for point in grid.points():
        tile = grid[point]
        if tile == Grid.TREE:
            tree += 1
        elif tile == Grid.LUMBER:
            lumber += 1

    return tree * lumber


def part_1(grid, end=10):
    grid = simulate(grid, end=end, print_turns=False)
    print("part 1:", value(grid))


def part_2(grid, end=1000000000):
    seen_tiles = []
    gen = 0

    while gen <= end:
        if grid.tiles in seen_tiles:
            print("cycle found at gen:", gen)
            break
        else:
            seen_tiles.append(grid.tiles)
            gen += 1
            grid = tick(grid)

        if (gen % 100) == 0:
            print("gen:", gen)

    cycle_start = None
    cycle_end = gen

    for s, g in enumerate(seen_tiles):
        if g == grid.tiles:
            cycle_start = s

    end_gen = (end - cycle_start) % (cycle_end - cycle_start)
    end_grid = Grid()
    end_grid.tiles = seen_tiles[cycle_start + end_gen]

    print(cycle_start, cycle_end)

    score = value(end_grid)
    print("part 2:", score)


string = open(sys.argv[1], "r").read()

grid = Grid(string=string)

if len(sys.argv) == 3:
    end = int(sys.argv[2])
else:
    end = None

part_1(grid, 10)

part_2(grid)

