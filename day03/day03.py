import re

from collections import namedtuple, Counter


Claim = namedtuple("Claim", ["id", "x", "y", "h", "w"])


regex = re.compile(r"\#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def parse_claim(s):
    match = regex.match(s)
    return Claim(
        id=match.group(1),
        x=int(match.group(2)),
        y=int(match.group(3)),
        w=int(match.group(4)),
        h=int(match.group(5)),
    )


def count_uses(claims):
    counts = Counter()
    for claim in claims:
        for x in range(claim.x, claim.x + claim.w):
            for y in range(claim.y, claim.y + claim.h):
                counts[(x, y)] += 1
    return counts


claims = list(map(parse_claim, open("input.txt", "r").readlines()))

uses = count_uses(claims)

overlap = 0
for coord in uses:
    if uses[coord] > 1:
        overlap += 1

print(overlap)
