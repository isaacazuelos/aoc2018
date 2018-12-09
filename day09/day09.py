from collections import namedtuple, defaultdict, Counter
from itertools import repeat


def part_1(player_count, last_marble_points, ret=False, print_status=False):
    scores = Counter()
    circle = []
    current_player = 0
    current_marble = 0  # this is the cursor

    # lnrm = lowest numbered remaining marble
    for lnrm in range(0, last_marble_points + 1):  # want that last marble!

        if (lnrm % 100_000) == 0:
            print(f"turn {lnrm} of {last_marble_points}")

        # insert marble
        if lnrm == 0:
            circle = [lnrm]
            current_marble = 0
        elif (lnrm % 23) == 0:
            current_marble = (current_marble - 7) % len(circle)
            removed = circle[current_marble]
            del circle[current_marble]
            scores[current_player] += lnrm + removed
        else:
            current_marble = (current_marble + 2) % len(circle)
            circle.insert(current_marble, lnrm)

        # print(
        #     f"""[{current_player}]
        #     lnrm: {lnrm},
        #     current: {current_marble}
        #     circle: {circle}"""
        # )

        current_player += 1
        if current_player > player_count:
            current_player = 1

    winner = scores.most_common(1)
    if ret:
        return winner
    else:
        print(f"part 1: {winner}")


def part_2(player_count, last_points):
    winner = part_1(player_count, last_points * 100, ret=True, print_status=True)
    print(f"part 2: {winner}")


examples = open("input.txt", "r").readlines()

for example in examples:
    words = example.split()
    player_count = int(words[0])
    last_points = int(words[-2])
    part_1(player_count, last_points)
    part_2(player_count, last_points)
