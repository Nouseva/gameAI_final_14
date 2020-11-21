#!/usr/bin/env python
"""
Misc utilities functions

"""
try:
    import os
    import pygame
except ImportError as err:
    print("couldn't load module from {}. {}".format(__name__, err))
    sys.exit(2)


def load_image(name, colorkey=None):
    fullname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    #"""
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    #"""

    # image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):

    class NoneSound:
        def play(self): pass
    if not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)

    return sound