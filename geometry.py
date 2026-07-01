import math

def distance_between_points(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return round(distance, 2)

def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (round(mx, 2), round(my,2))

def slope(x1, y1, x2, y2):
    if x2 - x1 == 0:
        return "Undefined"
    m = (y2 - y1) / (x2 - x1)
    return round(m, 2)
