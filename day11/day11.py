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


grid_serial_number = 5719
size = 300

power_levels = [list(repeat(0, size)) for _ in range(size)]

for x in range(len(power_levels)):
    for y in range(len(power_levels)):
        power_levels[x][y] = power_level(x, y, grid_serial_number)

print("part 1:", part_1(power_levels))

