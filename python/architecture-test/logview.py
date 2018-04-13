"""Log module."""
import pygame
from enum import Enum
import os

import constants as cons


class MsgType(Enum):
    """Message type enumeration."""

    INFO = 0
    DEBUG = 1
    BATTLE = 2


class LogView():
    """Log class which filters all incoming messages and prints the ones
    we currently want to see based on various toggles."""
    def __init__(self, surface, pos_rect):
        """Construct a log."""
        self.surface = surface
        self.topleft = pos_rect
        self.dirty = True
        self.message_list = list()

    def post(self, message, logtype):
        """Post a message to the log with a corresponding message type."""
        print(message)
        self.message_list.append(Message(message, logtype))
        self.dirty = True

    def draw(self, screen):
        """Blit what we want to see on the main screen."""
        if self.dirty:
            # Fill with black first
            self.surface.fill(pygame.color.Color("black"))
            # Blit messages first
            for message in self.message_list:
                message.draw(self.surface)
            # Blit to main screen last
            screen.blit(self.surface, self.topleft)
            self.dirty = False


class Message():
    """A message which fits the Log-view."""
    def __init__(self, text, logtype):
        self.x = cons.LOG_POS.x
        self.y = cons.LOG_POS.y
        self.width = cons.LOG_POS.width
        self.height = cons.LOG_POS.height
        print(cons.LOG_POS)
        self.text = text
        self.type = logtype
        path = os.path.join('Avara.otf')
        self.font = pygame.font.Font(path, cons.TILE_D//2)
        self.color = self.set_color()
        self.textsurf = self.generate_surface(text)

    def set_color(self):
        """Set the color based on what type it is."""
        if self.type == MsgType.INFO:
            return pygame.color.Color('white')
        if self.type == MsgType.DEBUG:
            return pygame.color.Color('lightblue')
        if self.type == MsgType.BATTLE:
            return pygame.color.Color('red')

    def generate_surface(self, text):
        """Return a surface which can hold the text."""
        lines = self.wrap_text(text)
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
                if self.font.size(line[:next])[0] <= self.width:
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
        with no background colour, and return the result.
        """
        rendered = [self.font.render(line, True, self.color).convert_alpha()
                    for line in lines]

        line_height = self.font.get_linesize()
        width = max(line.get_width() for line in rendered)
        tops = [int(round(i * line_height)) for i in range(len(rendered))]
        height = tops[-1] + self.font.get_height()

        surface = pygame.Surface((width, height)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for y, line in zip(tops, rendered):
            surface.blit(line, (0, y))

        return surface

    def draw(self, surface):
        """Draw the text."""
        print(self.color)
        surface.blit(self.textsurf, (0, 0))
