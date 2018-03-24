class Shadow():
    """Reperesent a shadow line."""

    def __init__(self, start, end):
        """Shadow line going from start to end."""
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start}, {self.end}"

    def contains(self, other):
        """Return true if other is completely covered by this one."""
        return self.start <= other.start and self.end >= other.end


class ShadowLine():
    """Represent a line of Shadow-objects."""

    def __init__(self):
        """Is basically a list."""
        self.shadows = list()

    def __repr__(self):
        return str(self.shadows)

    def is_in_shadow(self, projection):
        """Return true if any shadow in the line covers the tile."""
        for shadow in self.shadows:
            if shadow.contains(projection):
                return True
        return False

    def add(self, newshadow):
        """Figure out where to slot the new shadow in the list."""
        index = 0
        for index, shadow in enumerate(self.shadows):
            # Stop when we hit the insertion point.
            if shadow.start >= newshadow.start:
                break
            else:
                index = 0
                break

        # The new shadow is going here. See if it overlaps the
        # previous or next.
        overlappingPrevious = False
        if (index > 0) and (self.shadows[index - 1].end > newshadow.start):
            overlappingPrevious = self.shadows[index - 1]

        overlappingNext = False
        if (index < len(self.shadows)) and (self.shadows[index].start < newshadow.end):
            overlappingNext = self.shadows[index]

        # Insert and unify with overlapping shadows.
        if overlappingNext:
            if overlappingPrevious:
                # Overlaps both, so unify one and delete the other.
                overlappingPrevious.end = overlappingNext.end
                del self.shadows[index]
            else:
                # Overlaps the next one, so unify it with that.
                overlappingNext.start = newshadow.start
        else:
            if overlappingPrevious:
                # Overlaps the previous one, so unify it with that.
                overlappingPrevious.end = newshadow.end
            else:
                # Does not overlap anything, so insert.
                self.shadows.insert(index, newshadow)

    def is_full_shadow(self):
        """Return true if whole row is in shadow."""
        length = len(self.shadows)
        start = self.shadows[0].start
        end = self.shadows[0].end
        print(f"length: {length} - start: {start} - end: {end}")
        if (length == 1) and (start == 0) and (end == 1):
            return True
        return False
