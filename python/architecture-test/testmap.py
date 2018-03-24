"""Module containing various utility-functions.

get_testmap() - Loads a map from a .txt file.
get_testmap_tiny() - Makes a map type list directly for debugging.
"""


def get_testmap_tiny():
    """Load this tiny map for debugging purposes."""
    testmap = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
               0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return testmap
