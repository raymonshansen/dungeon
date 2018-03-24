import pygame
import os

from tiletypes import get_filenames


class TypeBank():
    def __init__(self):
        self.filenames = get_filenames()
        self.images = list()
        self.load_all()

    def load_all(self):
        for key in self.filenames:
            # print(f"loading: {self.filenames[key]}")
            path = os.path.join('tiles', self.filenames.get(key, 'none.png'))
            img = pygame.image.load(path).convert_alpha()
            self.images.append(img)

    def get_type(self, idx):
        return self.images[idx]
