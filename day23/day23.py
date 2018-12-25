import re
import sys

from collections import namedtuple

Bot = namedtuple("Bot", ["x", "y", "z", "r"])

BOT_RE = re.compile(r"pos=<(\-?\d+),(\-?\d+),(\-?\d+)>, r=(\-?\d+)")
def parse_line(line):
    match = BOT_RE.match(line)
    return Bot(x=int(match.group(1)), y=int(match.group(2)), z=int(match.group(3)), r=int(match.group(4)))

def distance(a, b):
   return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def part_1(bots):
    strongest = max(bots, key=lambda b: b.r)
    in_range = sum(map(lambda b: distance(strongest, b) <= strongest.r, bots))

    print("part 1:", in_range)

def space_size(bots):


    bx = max(bots, key=lambda b: b.x)
    sx = min(bots, key=lambda b: b.x)
    by = max(bots, key=lambda b: b.y)
    sy = min(bots, key=lambda b: b.y)
    bz = max(bots, key=lambda b: b.z)
    sz = min(bots, key=lambda b: b.z)
    
    x = bx.x - sx.x
    y = by.y - sy.y
    z = bz.z - sz.z

    print("search space size:", x * y * z)

def part_2(bots):
    in_range = { }
    for bot in bots:
        in_range[bot] = sum(map(lambda b: distance(bot, b) <= bot.r, bots))

    in_range = (sorted(bots, reverse=True, key=lambda b: in_range[b]))[0:3]

    space_size(in_range)
    print("part 2", "unimplemented")

bots = list(map(parse_line, open(sys.argv[1], 'r').read().split("\n")))

part_1(bots)
space_size(bots)
part_2(bots)