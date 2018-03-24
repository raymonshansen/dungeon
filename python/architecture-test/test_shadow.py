import unittest
from shadow import Shadow, ShadowLine


class TestShadow(unittest.TestCase):
    def test_valid_constructor(self):
        """Shadow initializes with given values."""
        start, end = 0, 1
        shadow = Shadow(start, end)
        self.assertEqual(shadow.start, start)
        self.assertEqual(shadow.end, end)

    def test_handles_invalid_parameters_gracefully(self):
        """Shadow start should be less than shadow end."""
        start, end = 0.5, 0
        shadow = Shadow(start, end)
        self.assertEqual(shadow.start, end)
        self.assertEqual(shadow.end, start)

    def test_equality(self):
        """Two Shadows with the same starting
        and ending points are considered equal."""
        first = Shadow(0, 1)
        second = Shadow(0, 1)
        self.assertEqual(first, second)

    def test_repr_is_evalable(self):
        """The __repr__ of an instance should return a string
        that could be evaluated to reconstruct the instance.
        """
        shadow = Shadow(0, 0.25)
        self.assertEqual(shadow, eval(repr(shadow)))

    def test_shadows_can_cover_other_shadows(self):
        """ A Shadow X covers another Shadow Y if:
        - X starts before or at the same place as Y
        - X ends after or at the same place as Y
        """
        bigger = Shadow(0, 0.7)
        smaller = Shadow(0.2, 0.6)
        also_small = Shadow(0.2, 0.3)
        self.assertTrue(bigger.covers(smaller))
        self.assertFalse(smaller.covers(bigger))
        self.assertTrue(smaller.covers(also_small))

    def test_shadows_can_overlap(self):
        """A Shadow X overlaps with Shadow Y if:
        - X ends after Y starts AND Y starts before X ends
        """
        first = Shadow(0, 0.4)
        second = Shadow(0.4, 0.8)
        third = Shadow(0.81, 0.95)
        self.assertTrue(first.adjacent(second))
        self.assertTrue(second.adjacent(first))
        self.assertFalse(second.adjacent(third))

    def test_shadows_do_not_always_overlap(self):
        """ Distinct Shadows should not overlap."""
        first = Shadow(0, 0.1)
        second = Shadow(0.3, 0.4)
        self.assertFalse(first.adjacent(second))

    def test_sortable(self):
        """Shadows can be sorted by their starting points."""
        first = Shadow(0, 0.1)
        second = Shadow(0.1, 0.2)
        third = Shadow(0.2, 0.3)
        expected = [first, second, third]
        actual = sorted([third, first, second])
        self.assertListEqual(expected, actual)


class TestShadowLine(unittest.TestCase):
    def test_valid_constructor(self):
        "NOTE: Constructor could be changed to take an iterable of Shadows."
        line = ShadowLine()
        self.assertTrue(line)

    def test_initializes_with_shadows(self):
        "Init takes an iterable of Shadows."
        shadows = [Shadow(0, 1), Shadow(3, 5)]
        actual = ShadowLine(shadows)

        expected = ShadowLine()
        for shadow in shadows:
            expected.add(shadow)

        self.assertEqual(expected, actual)

    def test_repr_is_evalable(self):
        """The __repr__ of an instance should return a string
        that could be evaluated to reconstruct the instance.
        """
        line = ShadowLine([Shadow(0, 1)])
        self.assertEqual(line, eval(repr(line)))

    def test_coalesces_two_overlapping_shadows(self):
        """Two Shadows that overlap are coalesced
        into a single Shadow.
        [0, 0.1]
        +  [0.1, 0.2] =
        [0,      0.2]
        """
        actual = ShadowLine([Shadow(0, 0.1)])
        actual.add(Shadow(0.1, 0.2))

        expected = ShadowLine([Shadow(0, 0.2)])
        self.assertEqual(expected, actual)

    def test_coalesces_multiple_overlapping_shadows(self):
        """Adding a Shadow that creates overlap between
        previously non-contiguous shadows should coalesce
        all three into one big Shadow.
        [0, 0.1]
        +         [0.3, 0.4] =
        [0, 0.1], [0.3, 0.4]

        +  [0.1,   0.3]      =
        [0,             0.4]
        """
        actual = ShadowLine([Shadow(0, 0.1)])
        actual.add(Shadow(0.3, 0.4))
        actual.add(Shadow(0.1, 0.3))

        expected = ShadowLine([Shadow(0, 0.4)])
        self.assertEqual(expected, actual)

    def test_only_coalesces_adjacent_shadows(self):
        """
        [0, 0.1]
        +                   [0.4, 0.5]  =
        [0, 0.1],           [0.4, 0.5]

        +         [0.2,      0.4]      =
        [0, 0.1], [0.2            0.5]
        """
        actual = ShadowLine([Shadow(0, 0.1)])
        actual.add(Shadow(0.4, 0.5))
        actual.add(Shadow(0.2, 0.4))

        expected = ShadowLine([Shadow(0.0, 0.1), Shadow(0.2, 0.5)])
        self.assertEqual(expected, actual)

    def test_can_tell_if_it_covers_a_tile(self):
        """The ShadowLine can tell if it covers a given tile."""
        line = ShadowLine([Shadow(0, 0.2), Shadow(0.5, 1.0)])

        projected_into_darkness = Shadow(0, 0.1)
        projected_into_light = Shadow(0.3, 0.4)

        self.assertTrue(line.is_in_shadow(projected_into_darkness))
        self.assertFalse(line.is_in_shadow(projected_into_light))

    def test_can_tell_if_entire_row_is_shadow(self):
        """Can tell if the entire row is visible"""
        line = ShadowLine()
        # First quarter covered:
        line.add(Shadow(0, 0.25))
        self.assertFalse(line.is_full_shadow())
        # Add last quarter, half covered:
        line.add(Shadow(0.75, 1))
        self.assertFalse(line.is_full_shadow())

        # Add the missing two middle quarters, fully covered:
        line.add(Shadow(0.25, 0.75))
        self.assertTrue(line.is_full_shadow())

    def test_handles_many_shadows(self):
        # Try permuting the order to ensure that it does not matter
        shadows = [
            Shadow(0, 0.1),
            Shadow(0.05, 0.08),
            Shadow(0.125, 0.175),
            Shadow(0.2, 0.325),
            Shadow(0.5, 0.55),
            Shadow(0.275, 0.450),
            Shadow(0.6, 0.8),
            Shadow(0.3, 0.99)
        ]
        line = ShadowLine()
        for shadow in shadows:
            line.add(shadow)

        self.assertFalse(line.is_full_shadow())
