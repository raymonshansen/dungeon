class Shadow():
    """Represent a Shadow."""

    def __init__(self, start, end):
        """Shadow covers tiles from start to end."""
        self.start = min(start, end)
        self.end = max(start, end)

    def __repr__(self):
        return f"Shadow({self.start}, {self.end})"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.start <= other.start

    def __add__(self, other):
        return Shadow(min(self.start, other.start), max(self.end, other.end))

    def covers(self, other):
        """Return True if other is completely covered by this one."""
        return self.start <= other.start and self.end >= other.end

    def adjacent(self, other):
        """Return True if other and self are adjacent
        or have any overlapping area."""
        return other.start <= self.end or self.start >= other.end


class ShadowLine():
    """Represent a line of Shadow-objects."""

    def __init__(self, shadows=None):
        """Is basically a list."""
        self.shadows = list()
        incoming = shadows or list()
        for shadow in incoming:
            self.add(shadow)

    def __repr__(self):
        return "ShadowLine([{}])".format(", ".join(repr(x) for x in self.shadows))

    def __eq__(self, other):
        return len(self.shadows) == len(other.shadows) and \
            all(x == y for x, y in zip(self.shadows, other.shadows))

    def is_in_shadow(self, projection):
        """Return true if any shadow in the line covers the tile."""
        return any(shadow.covers(projection) for shadow in self.shadows)

    def contains_overlap(self):
        for x in range(1, len(self.shadows)):
            prev = self.shadows[x - 1]
            curr = self.shadows[x]
            if prev.adjacent(curr):
                return True
        return False

    def coalesce(self):
        while self.contains_overlap():
            new_shadows = list()
            for x, y in zip(self.shadows, self.shadows[1:]):
                if x.adjacent(y):
                    new_shadows.append(x + y)
                else:
                    new_shadows.append(x)
            self.shadows = new_shadows

    def add(self, newshadow):
        """Add a new Shadow to the line,
        coalescing it into a bigger shadow if."""
        self.shadows = sorted(self.shadows + [newshadow])
        self.coalesce()

    def is_full_shadow(self):
        """Return true if whole row is in shadow."""
        length = len(self.shadows)
        start = self.shadows[0].start
        end = self.shadows[0].end
        print(f"length: {length} - start: {start} - end: {end}")
        return length == 1 and start == 0 and end == 1
