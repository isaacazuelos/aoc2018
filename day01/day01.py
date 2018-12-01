from itertools import cycle

lines = open("input.txt", "r").readlines()
nums = list(int(l) for l in lines)

print(f"part 1: {sum(nums)}")

seen = set()
acc = 0

for n in cycle(nums):
    seen.add(acc)
    acc += n
    if acc in seen:
        break

print(f"part 2: {acc}")
