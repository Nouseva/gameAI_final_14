
import pygame.sprite

from . import utils

class Agent(pygame.sprite.Sprite):
    """
    An agent is something in the world that does something
    Enemy, game/player character

    Agents must define Agent.getAction method,
    but can otherwise overwrite any other methods.

    Methods must assume that they are working with shalow copies of data
    Deep copies must be made of anything they want to keep

    
    """

    def __init__(self, image, pos = None, index = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image, -1)
        if pos:
            self.rect = self.rect.move(pos)
        self.index = index
        # self.bump  = utils.load_sound('collision.ogg')

    def update(self, action, walls):
        """Move based on the action that was given

        Args:
            action (tuple): a direction normalized to a maze step
            walls (list): Rects which are the maze walls

        Returns:
            : False if action will cause agent to collide with walls, True otherwise

        """
        self.rect = self.rect.move(action)
        collision = self.rect.collidelist(walls)
        if collision == -1:
            pass
            # TODO: behavior when agent collides with wall
            # maybe never executed since ai controlled but w/e
            # self.bump.play() # Hit wall
        return collision
    
    def getRect(self):
        return self.rect