from itertools import repeat
from collections import defaultdict, Counter


def distance(a, b):
    """ Manthatten distance """
    (ax, ay) = a
    (bx, by) = b
    return abs(ax - bx) + abs(ay - by)


def points_in_grid(w, h):
    for x in range(w):
        for y in range(h):
            yield (x, y)


def on_edge(coord, w, h):
    (x, y) = coord
    return (x == 0) or (y == 0) or (x == w) or (y == h)


def closest_coord(point, coords):
    distances = {}
    for coord in coords:
        dist = distance(coord, point)
        distances[coord] = dist

    m = min(distances.values())
    closest_coords = []
    for c, d in distances.items():
        if d == m:
            closest_coords.append(c)

    if len(closest_coords) == 1:
        return closest_coords[0]
    else:
        return None


lines = open("input.txt", "r").read().split("\n")

coords = []
for line in lines:
    [x, y] = line.split(",")
    coords.append((int(x), int(y)))


h = max(x for (x, y) in coords) + 1
w = max(x for (x, y) in coords) + 1


def part_1(coords, w, h):

    areas = Counter()
    for point in points_in_grid(w, h):
        closest = closest_coord(point, coords)
        if closest:
            areas[closest] += 1
            # make the area so small it loses and isn't counted
            if on_edge(point, w, h):
                areas[closest] -= (h * w) ** 16

    answer = areas.most_common(1)[0][1]  # (coord, area) for coord with highest area

    print(f"part 1: {answer}")


def part_2(coords, w, h, max_total_dist_sum):
    point_count = 0
    for point in points_in_grid(w, h):
        dist_sum = 0
        for coord in coords:
            dist_sum += distance(coord, point)
        if dist_sum < max_total_dist_sum:
            point_count += 1

    answer = point_count
    print(f"part 2: {answer}")


part_1(coords, w, h)
part_2(coords, w, h, 10000)
