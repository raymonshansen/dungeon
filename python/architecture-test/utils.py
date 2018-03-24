"""Utility functions."""


def plot_line(x1, y1, x2, y2):
    """Brensenham line drawing algorithm.

    Return a list of points(tuples) along the line.
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
    pixelpoints = [(x, y)]

    if dx > dy:
        fraction = dy - (dx/2)
        while x is not x2:
            if fraction >= 0:
                y = y + stepy
                fraction = fraction - dx
            x = x + stepx
            fraction = fraction + dy
            pixelpoints.append((x, y))
    else:
        fraction = dx - (dy/2)
        while y is not y2:
            if fraction >= 0:
                x = x + stepx
                fraction = fraction - dy
            y = y + stepy
            fraction = fraction + dx
            pixelpoints.append((x, y))
    return pixelpoints


def plot_circle(x0, y0, radius):
    """Return a list of the points around a circle."""
    result = []
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    result.append((x0, y0 + radius))
    result.append((x0, y0 - radius))
    result.append((x0 + radius, y0))
    result.append((x0 - radius, y0))

    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        result.append((x0 + x, y0 + y))
        result.append((x0 - x, y0 + y))
        result.append((x0 + x, y0 - y))
        result.append((x0 - x, y0 - y))
        result.append((x0 + y, y0 + x))
        result.append((x0 - y, y0 + x))
        result.append((x0 + y, y0 - x))
        result.append((x0 - y, y0 - x))

    return result
