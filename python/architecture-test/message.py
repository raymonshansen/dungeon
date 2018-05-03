"""Message Module"""
import pygame
import os
from enum import Enum

import constants as cons


class MsgType(Enum):
    """Message type enumeration."""

    INFO = 0
    DEBUG = 1
    BATTLE = 2


class Message():
    """A message which fits the Log-view."""
    def __init__(self, text, logtype):
        self.rect = pygame.Rect(0, 0, cons.LOG_DIM[0], cons.LOG_DIM[1])
        self.text = text
        self.type = logtype
        self.path = os.path.join('Avara.otf')
        self.font = pygame.font.Font(self.path, cons.LOG_FONTSIZE)
        self.color = self.set_color()
        self.bgcolor = None
        self.textsurf = self.generate_surface()

    def set_size(self, size):
        self.font = pygame.font.Font(self.path, size)

    def set_bgcolor(self, color):
        """Set the background color for the text surface."""
        self.bgcolor = color
        self.textsurf = self.generate_surface()

    def get_surface(self):
        """Return the text surface."""
        return self.textsurf

    def get_height(self):
        """Return the hight of the textsurf in pixels."""
        return self.textsurf.get_height()

    def set_color(self):
        """Set the color based on what type it is."""
        if self.type == MsgType.INFO:
            return pygame.color.Color('antiquewhite')
        if self.type == MsgType.DEBUG:
            return pygame.color.Color('lightblue')
        if self.type == MsgType.BATTLE:
            return pygame.color.Color('firebrick')

    def generate_surface(self):
        """Return a surface which can hold the text."""
        lines = self.wrap_text(self.text)
        return self.render_text_list(lines)

    def wrap_text(self, text):
        """Wrap text to fit inside a given width when rendered."""
        text_lines = text.replace('\t', '    ').split('\n')

        wrapped_lines = []
        for line in text_lines:
            line = line.rstrip() + ' '
            if line == ' ':
                wrapped_lines.append(line)
                continue

            # Get the leftmost space ignoring leading whitespace
            start = len(line) - len(line.lstrip())
            start = line.index(' ', start)
            while start + 1 < len(line):
                # Get the next potential splitting point
                next = line.index(' ', start + 1)
                if self.font.size(line[:next])[0] <= self.rect.width:
                    start = next
                else:
                    wrapped_lines.append(line[:start])
                    line = line[start+1:]
                    start = line.index(' ')
            line = line[:-1]
            if line:
                wrapped_lines.append(line)
        return wrapped_lines

    def render_text_list(self, lines):
        """Draw multiline text to a single surface with a transparent background.
        Draw multiple lines of text in the given font onto a single surface
        with no background color, and return the result.
        """

        rendered = [self.font.render(line, True, self.color, self.bgcolor)
                    for line in lines]

        line_height = self.font.get_linesize()
        width = max(line.get_width() for line in rendered)
        tops = [int(round(i * line_height)) for i in range(len(rendered))]
        height = tops[-1] + self.font.get_height()
        self.rect.height = height

        surface = pygame.Surface((width, height)).convert_alpha()
        for y, line in zip(tops, rendered):
            surface.blit(line, (0, y))

        return surface

    def draw(self, surface):
        """Draw the text."""
        surface.blit(self.textsurf, (5, self.rect.y))
