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
    def __init__(self, surface, rect):
        """Construct a log."""
        self.surface = surface
        self.rect = rect
        self.dirty = True
        self.message_list = list()

    def post(self, message, logtype):
        """Post a message to the log with a corresponding message type."""
        self.message_list.append(Message(message, logtype))
        self.dirty = True

    def draw_messages(self):
        """Calculates how many of the messages in the list that fit on the
        log-view, and blit them."""
        current_y = self.rect.height
        for message in reversed(self.message_list):
            current_y -= message.get_height()
            if current_y < 0:
                break
            message.rect.y = current_y
            message.draw(self.surface)

    def draw(self, screen):
        """Blit what we want to see on the main screen."""
        if self.dirty:
            # Fill with black first
            self.surface.fill(pygame.color.Color("black"))
            # Blit messages first
            self.draw_messages()
            # Draw border-line
            linecol = pygame.color.Color('antiquewhite')
            start_pos = (0, 0)
            end_pos = (0, self.rect.height)
            pygame.draw.line(self.surface, linecol, start_pos, end_pos, 1)
            # Blit to main screen last
            screen.blit(self.surface, self.rect)
            self.dirty = False


class Message():
    """A message which fits the Log-view."""
    def __init__(self, text, logtype):
        self.rect = pygame.Rect(0, 0, cons.LOG_DIM[0], cons.LOG_DIM[1])
        self.text = text
        self.type = logtype
        path = os.path.join('Avara.otf')
        self.font = pygame.font.Font(path, cons.TILE_D//2)
        self.color = self.set_color()
        self.textsurf = self.generate_surface(text)

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
        rendered = [self.font.render(line, True, self.color).convert_alpha()
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
