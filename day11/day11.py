def hundreds_digit(n):
    if n < 100:
        return None
    return ((abs(n) % 1000) - (abs(n) % 100)) // 100


def power_level(point, grid_serial_number):
    (x, y) = point
    rack_id = x + 10
    power_level = ((rack_id * y) + grid_serial_number) * rack_id
    return hundreds_digit(power_level) - 5

def point_in_grid_one_based(w, h):
    for y in range(1, h+1):
        for x in range(1, w+1):
            yield (x, y)

def part_1(width, height, power_levels):
    max_power_seen = 0
    point_for_square_with_max_power = None
    for point in point_in_grid_one_based(width - 2, height - 2):
        power_for_square = 0
        
        (x, y) = point
        for dx in range(0, 3):
            for dy in range(0, 3):
                power_for_square += power_levels[(x + dx, y + dy)]


        if power_for_square > max_power_seen:
            max_power_seen = power_for_square
            point_for_square_with_max_power = point
    
    return point_for_square_with_max_power

grid_serial_number = 5719
width = 300
height = 300

power_levels = {point: power_level(point, grid_serial_number) for point in point_in_grid_one_based(width, height)}

def print_grid(power_levels, x, y, h, w):
    for dy in range(0, w):
        for dx in range(0, h):
            print(power_levels[(x+dx, y+dy)], end=" ")
        print("")

print(print_grid(power_levels, 32, 44, 5, 5))
print("part 1:", part_1(width, height, power_levels))

