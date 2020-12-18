import pygame.sprite

from . import utils

class Coin(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = utils.load_image('coin.png', scale = tile_size,)
        self.rect = self.rect.move((tile_size[0] * position[0], tile_size[1] * position[1]))
    pass

class Boost_S(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('small_boost.png', scale = tile_size)
        self.rect = self.rect.move((tile_size[0] * position[0], tile_size[1] * position[1]))

class Boost_L(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('large_boost.png', scale = tile_size)
        self.rect = self.rect.move((tile_size[0] * position[0], tile_size[1] * position[1]))

