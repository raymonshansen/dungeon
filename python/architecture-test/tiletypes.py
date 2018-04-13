"""Contains functions to mangae tiletypes."""

from enum import Enum, IntEnum


def get_filenames():
    """Tile-filename dictionary."""
    filenames = {0: "none.png",
                 1: "floor.png",
                 2: "wall.png",
                 3: "dark.png"}
    return filenames


"""
translate_dict = {1: 47, 2: 44, 3: 44, 4: 46, 5: 45,
                  6: 44, 7: 44, 8: 38, 9: 38, 10: 36,
                  11: 36, 12: 37, 13: 37, 14: 36, 15: 36,
                  16: 30, 17: 29, 18: 28, 19: 28, 20: 30,
                  21: 29, 22: 28, 23: 28, 24: 16, 25: 16,
                  26: 15, 27: 15, 28: 16, 29: 16, 30: 16,
                  31: 16, 32: 43, 33: 42, 34: 39, 35: 39,
                  36: 25, 37: 40, 38: 39, 39: 39, 40: 38,
                  41: 38, 42: 36, 43: 36, 44: 37, 45: 37,
                  46: 36, 47: 36, 48: 19, 49: 18, 50: 17,
                  51: 17, 52: 19, 53: 18, 54: 17, 55: 17,
                  56: 16, 57: 16, 58: 15, 59: 15, 60: 16,
                  61: 16, 62: 16, 63: 15, 64: 14, 65: 13,
                  66: 10, 67: 10, 68: 12, 69: 11, 70: 10,
                  71: 10, 72: 9, 73: 9, 74: 7, 75: 7,
                  76: 8, 77: 9, 78: 7, 79: 7, 80: 6,
                  81: 5, 82: 4, 83: 4, 84: 6, 85: 5,
                  86: 4, 87: 4, 88: 3, 89: 3, 90: 49,
                  91: 49, 92: 3, 93: 3, 94: 49, 95: 49,
                  96: 14, 97: 13, 98: 10, 99: 10, 100: 12,
                  101: 11, 102: 10, 103: 10, 104: 9, 105: 9,
                  106: 7, 107: 7, 108: 8, 109: 8, 110: 7,
                  111: 7, 112: 6, 113: 5, 114: 4, 115: 4,
                  116: 6, 117: 5, 118: 4, 119: 4, 120: 3,
                  121: 3, 122: 49, 123: 49, 124: 3, 125: 3,
                  126: 49, 127: 49, 128: 35, 129: 32, 130: 31,
                  131: 31, 132: 33, 133: 48, 134: 31, 135: 31,
                  136: 22, 137: 22, 138: 20, 139: 20, 140: 21,
                  141: 21, 142: 20, 143: 20, 144: 30, 145: 29,
                  146: 28, 147: 28, 148: 30, 149: 29, 150: 28,
                  151: 28, 152: 16, 153: 16, 154: 15, 155: 15,
                  156: 16, 157: 16, 158: 15, 159: 15, 160: 27,
                  161: 27, 162: 23, 163: 23, 164: 24, 165: 24,
                  166: 23, 167: 23, 168: 22, 169: 22, 170: 20,
                  171: 20, 172: 21, 173: 21, 174: 20, 175: 20,
                  176: 19, 177: 18, 178: 17, 179: 17, 180: 19,
                  181: 18, 182: 17, 183: 17, 184: 16, 185: 16,
                  186: 15, 187: 15, 188: 16, 189: 16, 190: 15,
                  191: 15, 192: 14, 193: 13, 194: 10, 195: 10,
                  196: 12, 197: 11, 198: 10, 199: 10, 200: 9,
                  201: 9, 202: 7, 203: 7, 204: 8, 205: 8,
                  206: 7, 207: 7, 208: 6, 209: 5, 210: 4,
                  211: 4, 212: 6, 213: 5, 214: 4, 215: 4,
                  216: 3, 217: 8, 218: 49, 219: 49, 220: 3,
                  221: 3, 222: 49, 223: 49, 224: 14, 225: 13,
                  226: 10, 227: 10, 228: 12, 229: 11, 230: 10,
                  231: 10, 232: 9, 233: 9, 234: 7, 235: 7,
                  236: 8, 237: 8, 238: 7, 239: 7, 240: 6,
                  241: 5, 242: 4, 243: 4, 244: 6, 245: 5,
                  246: 4, 247: 4, 248: 3, 249: 3, 250: 49,
                  251: 49, 252: 3, 253: 3, 254: 49, 255: 49
                  }
"""


class TileStatus(Enum):
    """Tile-status enumeration."""

    UNEXPLORED = 1
    EXPLORED = 2
    VISIBLE = 3


class TileTypes(IntEnum):
    """Tile-type enumeration."""

    NONE = 0
    FLOOR = 1
    WALL = 2
    DARK = 3
