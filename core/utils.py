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

def nearestPoint(pos):
    """
    Finds the nearest grid point to a position (discretizes).
    """
    print(pos)
    (current_row, current_col) = pos

    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)

    return (grid_row, grid_col)

def pos_to_coord(pos, grid_size):
    """ Converts a position index of layout, to a pixel coordinate on the screen
    """

    pix_x = pos[0] * grid_size[0]
    pix_y = pos[1] * grid_size[1]

    return nearestPoint((pix_x, pix_y))

def matrixAsList(matrix, value = True):
    """
    Turns a matrix into a list of coordinates matching the specified value
    """

    rows, cols = len(matrix), len(matrix[0])
    cells = []
    for row in range(rows):
        for col in range(cols):
            if (matrix[row][col] == value):
                cells.append((row, col))

    return cells

def buildHash(*args):
    """
    Build a hash code from different components.
    """

    hashCode = INITIAL_HASH_VALUE

    for arg in args:
        hashCode = hashCode * HASH_MULTIPLIER + hash(arg)

    return int(hashCode)