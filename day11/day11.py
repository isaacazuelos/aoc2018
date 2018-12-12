from itertools import repeat


def hundreds_digit(n):
    if n < 100:
        return None
    return ((abs(n) % 1000) - (abs(n) % 100)) // 100


def power_level(x, y, grid_serial_number):
    rack_id = x + 10
    power_level = ((rack_id * y) + grid_serial_number) * rack_id
    return hundreds_digit(power_level) - 5


def print_grid(power_levels, x, y, h, w):
    for dy in range(0, w):
        for dx in range(0, h):
            print(power_levels[x + dx][y + dy], end=" ")
        print("")


def square(x, y, size, power_levels):
    power = 0
    for dx in range(0, size):
        for dy in range(0, size):
            power += power_levels[x + dx][y + dy]
    return power


def part_1(power_levels):
    highest_power = 0
    position = None

    for x in range(0, len(power_levels) - 1 - 2):
        for y in range(0, len(power_levels) - 1 - 2):
            power = square(x, y, 3, power_levels)
            if power > highest_power:
                highest_power = power
                position = (x, y)

    return (position, highest_power)


def part_2(power_levels):
    best_position = None
    best_size = None
    best_power = -1000

    max_size = len(power_levels)

    for x in range(0, max_size):
        print("on row", x)
        for y in range(0, max_size):
            # the sizes of the square is limited by where the coord is, since
            # it can't go past the edge.
            square_power = 0

            # for each valid size of square, we want to only add the new row and column
            size = 0
            while size + x < max_size and size + y < max_size:
                # add right column
                square_power += sum(
                    power_levels[x + size][y + dy] for dy in range(0, size + 1)
                )
                # add bottom row
                square_power += sum(
                    power_levels[x + dx][y + size] for dx in range(0, size + 1)
                )
                # remove overlapping bottom right square
                square_power -= power_levels[x + size][y + size]

                if square_power > best_power:
                    best_power = square_power
                    best_position = (x, y)
                    best_size = size + 1
                    print(f"new best at {x},{y},{best_size} with {best_power} ")

                size += 1

    return (best_position, best_size, best_power)


grid_serial_number = 5719
size = 300

power_levels = [list(repeat(0, size)) for _ in range(size)]

for x in range(len(power_levels)):
    for y in range(len(power_levels)):
        power_levels[x][y] = power_level(x, y, grid_serial_number)

ans1 = part_1(power_levels)
print(f"part 1: {ans1[0][0]},{ans1[0][1]}")
ans2 = part_2(power_levels)
print(f"part 2: {ans2[0][0]},{ans2[0][1]},{ans2[1]},")
