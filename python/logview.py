"""Log module."""
import pygame
from message import Message
import constants as cons


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
            message.rect.x = 12
            message.draw(self.surface)

    def draw(self, screen):
        """Blit what we want to see on the main screen."""
        if self.dirty:
            # Fill with black first
            self.surface.fill(pygame.color.Color("black"))
            # Blit messages first
            self.draw_messages()
            # Draw border-line
            linecol = cons.MAINMENU_SELECTED_COL
            start_pos = (0, 0)
            end_pos = (0, self.rect.height)
            pygame.draw.line(self.surface, linecol, start_pos, end_pos, 1)
            start_pos = (7, 7)
            end_pos = (7, self.rect.height - 7)            
            pygame.draw.line(self.surface, linecol, start_pos, end_pos, 1)
            # Blit to main screen last
            screen.blit(self.surface, self.rect)
