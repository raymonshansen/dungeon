import pygame

import constants as cons
from dungeon import Dungeon


class StatView():
    def __init__(self, surface, pos_rect):
        self.surface = surface
        self.topleft = pos_rect
        self.dirty = True

    def draw(self, screen):
        if self.dirty:
            self.surface.fill(pygame.color.Color("moccasin"))
            screen.blit(self.surface, self.topleft)


class Log():
    def __init__(self, surface, pos_rect):
        self.surface = surface
        self.topleft = pos_rect
        self.dirty = True

    def draw(self, screen):
        if self.dirty:
            self.surface.fill(pygame.color.Color("navajowhite"))
            screen.blit(self.surface, self.topleft)


class Game():
    def __init__(self):
        pygame.init()
        self.window_w = cons.TILE_D*cons.SCREEN_TW
        self.window_h = cons.TILE_D*cons.SCREEN_TH
        self.screensize = (self.window_w, self.window_h)
        self.screen = pygame.display.set_mode(self.screensize)
        self.running = True
        self.setup()

    def setup(self):
        dungeonsurface = pygame.Surface(cons.MAP_DIM)
        self.dungeon = Dungeon(dungeonsurface, cons.MAP_POS, 50, 50)
        statsurface = pygame.Surface(cons.STAT_DIM)
        self.statview = StatView(statsurface, cons.STAT_POS)
        logsurface = pygame.Surface(cons.LOG_DIM)
        self.logview = Log(logsurface, cons.LOG_POS)

        # Test player
        self.px = 25
        self.py = 25

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            # Quit the game.
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                break
            # Toggle fullscreen.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if self.screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(self.screensize)
                else:
                    pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
            
            # Move the player.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.py -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.py += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.px -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.px += 1

    def draw(self):
        self.dungeon.draw(self.screen, self.px, self.py)
        self.statview.draw(self.screen)
        self.logview.draw(self.screen)

    def loop(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.loop()
