from config import Point
"""Utility functions."""


def round_down(value, multiple):
    """Return value rounded down to closest multiple not zero."""
    return max((value - (value % multiple)), multiple)


def plot_line(x1, y1, x2, y2):
    """The classic Brensenham line drawing algorithm.
    Returns a list of points(tuples) along the line.
    """
    dx = x2 - x1
    dy = y2 - y1
    if dy < 0:
        dy = -dy
        stepy = -1
    else:
        stepy = 1
    if dx < 0:
        dx = -dx
        stepx = -1
    else:
        stepx = 1
    dy = dy*2
    dx = dx*2
    x = x1
    y = y1
    pixelpoints = [Point(x, y)]

    if dx > dy:
        fraction = dy - (dx/2)
        while x is not x2:
            if fraction >= 0:
                y = y + stepy
                fraction = fraction - dx
            x = x + stepx
            fraction = fraction + dy
            pixelpoints.append(Point(x, y))
    else:
        fraction = dx - (dy/2)
        while y is not y2:
            if fraction >= 0:
                x = x + stepx
                fraction = fraction - dy
            y = y + stepy
            fraction = fraction + dx
            pixelpoints.append(Point(x, y))
    pixelpoints.reverse()
    # print(pixelpoints)
    return pixelpoints
