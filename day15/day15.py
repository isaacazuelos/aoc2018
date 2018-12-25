import sys
from collections import deque
from itertools import product


class Grid:
    EMPTY_TILE = "."
    WALL_TILE = "#"
    GOBLIN_TILE = "G"
    ELF_TILE = "E"

    def __init__(self, string):
        self.tiles = []
        self._guys = set()
        self.load_from_string(string)

    @property
    def guys(self):
        """ This way all accesses to guys are sorted. """
        return list(sorted(self._guys, key=Guy.reading_order_key))

    def kill(self, guy):
        self._guys.remove(guy)

    def points(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                yield (x, y)

    def load_from_string(self, string):
        tiles = []

        y = 0
        for line in map(list, string.split("\n")):
            row = []
            x = 0
            for tile in line:
                if tile in [Grid.ELF_TILE, Grid.GOBLIN_TILE]:
                    self._guys.add(Guy((x, y), self, bad=(tile != Grid.ELF_TILE)))
                    row.append(Grid.EMPTY_TILE)
                else:
                    row.append(tile)
                x += 1
            tiles.append(row)
            y += 1

        self.tiles = tiles

    def __str__(self):
        res = []
        for pos in self.points():
            if pos[0] == 0:
                res.append("\n")

            guy = self.guy_at(pos)
            if not guy:
                tile = self[pos]
                res.append(tile)
            elif guy.bad:
                res.append(Grid.GOBLIN_TILE)
            else:
                res.append(Grid.ELF_TILE)

        return "".join(res)

    def __getitem__(self, pos):
        (x, y) = pos
        return self.tiles[y][x]

    def guy_at(self, pos):
        for guy in self.guys:
            if guy.position == pos:
                return guy

    @staticmethod
    def _construct_path(pos, parents):
        path = []
        cursor = pos

        while cursor is not None:
            path.append(cursor)
            cursor = parents[cursor]

        path.reverse()
        return path

    def shortest_path(self, start, end):
        # Thanks, wikipedia!
        open_set = deque([start])
        closed_set = set()
        parents = {start: None}

        while open_set:
            cursor = open_set.popleft()
            if cursor == end:
                return Grid._construct_path(cursor, parents)

            for child in self.open_adjacent_to(cursor):
                if child in closed_set:
                    continue

                if child not in open_set:
                    parents[child] = cursor
                    open_set.append(child)

            closed_set.add(cursor)

    def tick(self):
        for guy in self.guys:
            guy.act()

    def finished(self):
        for guy in self.guys:
            for other_guy in self.guys:
                if guy.is_enemy(other_guy):
                    return False
        return True

    def simulate(self, end=None, print_turns=False):
        i = 0

        while (not self.finished()) and ((not end) or i <= end):
            if print_turns:
                print("turn:", i)
                print(self)

            self.tick()
            i += 1

        if print_turns:
            print("turn:", i)
            print(self)

    @staticmethod
    def distance(a, b):
        (ax, ay) = a
        (bx, by) = b
        return abs(ax - bx) + abs(ay - by)

    @staticmethod
    def adjacent_to(position):
        (x, y) = position
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                # positions are not self-adjacent
                if dx != 0 or dy != 0:
                    yield (x + dx, y + dy)

    def open_adjacent_to(self, position):
        for adj in Guy.adjacent_to(position):
            if (self[adj] == Grid.EMPTY_TILE) and not self.guy_at(adj):
                yield adj


class Guy:
    def __init__(self, position, grid, hp=200, atk=3, bad=False):
        self.bad = bad
        self.position = position
        self.hp = hp
        self.atk = atk

        self.grid = grid

    def reading_order_key(self):
        (x, y) = self.position
        return (y, x)

    def hp_key(self):
        return self.hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.grid.kill(self)

    def act(self):
        if not self.adjacent_enemies():
            self.move()

        self.attack()

    def move(self):
        shortest_path_length = 2 ** 60
        shortest_path = None

        for enemy in self.enemies():
            for target in enemy.adjacent_open():
                path = self.grid.shortest_path(self.position, target)
                if path and len(path) < shortest_path_length:
                    shortest_path_length = len(path)
                    shortest_path = path

        print("path is ", shortest_path)
        self.position = shortest_path[1]

    def attack(self):
        target = min(self.adjacent_enemies(), default=None, key=Guy.hp_key)
        if target:
            target.take_damage(self.atk)

    def is_enemy(self, target):
        return self.bad != target.bad

    def enemies(self):
        return filter(self.is_enemy, self.grid.guys)

    @staticmethod
    def adjacent_to(position):
        (x, y) = position
        for (dx, dy) in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            (nx, ny) = (x + dx, y + dy)
            yield (nx, ny)

    def adjacent(self):
        return Guy.adjacent_to(self.position)

    def adjacent_enemies(self):
        enemies = []
        for pos in self.adjacent():
            guy = self.grid.guy_at(pos)
            if guy and self.is_enemy(guy):
                enemies.append(guy)
        return enemies

    def adjacent_open(self):
        for pos in self.adjacent():
            if self.grid[pos] == Grid.EMPTY_TILE and not self.grid.guy_at(pos):
                yield pos


string = open(sys.argv[1], "r").read()

grid = Grid(string)

if len(sys.argv) == 3:
    end = int(sys.argv[2])
else:
    end = None

grid.simulate(end=end, print_turns=True)
