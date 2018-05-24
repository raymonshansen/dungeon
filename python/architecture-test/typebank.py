import pygame
import os


class TypeBank():
    def __init__(self, loadfunc):
        self.filenames = loadfunc()
        self.images = list()
        self.load_all()

    def load_all(self):
        for key in self.filenames:
            path = os.path.join('tiles2', self.filenames.get(key, 'none.png'))
            img = pygame.image.load(path).convert_alpha()
            self.images.append(img)

    def get_type(self, tiletype):
        return self.images[tiletype]
