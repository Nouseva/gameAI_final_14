#!/usr/bin/env python

try:
    import sys
    import os
    import pygame

    from pygame.locals import *

    from core import utils
    from core.agent import Agent
    from core.layout import getLayout
    
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)

##### VARIABLES #####
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
BG_COLOR = 'black'
WALL_THICKNESS = 20
WALL_COLOR = 'white'
# DEFAULT_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')


def main():
    pygame.display.init()
    # pygame.mixer.quit() # Disable sound
    # print(pygame.mixer == None)
    surface_main = pygame.display.set_mode(SCREEN_SIZE)

    logo, _ = utils.load_image('test_icon.png', -1)
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    background = pygame.Surface(surface_main.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    foreground = pygame.Surface(surface_main.get_size())
    foreground = foreground.convert()

    walls = {
        tuple(pygame.Rect(0, 0, SCREEN_WIDTH, WALL_THICKNESS)) : 0, # Top wall
        tuple(pygame.Rect(0, 0, WALL_THICKNESS, SCREEN_HEIGHT)) : 1, # Left Wall
        tuple(pygame.Rect(0, SCREEN_HEIGHT-WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS)) : 2, # Bottom wall
        tuple(pygame.Rect(SCREEN_WIDTH-WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT)) : 3  # Right wall
    }

    for r in walls.keys():
        # print(r)
        pygame.draw.rect(foreground, WALL_COLOR, r)

    # Loading an in
    # ball_image, ball_rect  = utils.load_image('intro_ball.gif')
    ball = Agent('intro_ball.gif', pos=(WALL_THICKNESS, WALL_THICKNESS))
    ball_speed = [5, 5]
    # surface_mainMenu = pygame.Surface(SCREEN_SIZE)

    #surface_main.blit(ball_image, (50, 50))
    #pygame.display.flip()

    plain_sprites = pygame.sprite.RenderPlain(ball)
    clock = pygame.time.Clock()

    while 1:
        # Framerate controller
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Ball will only move when the mouse button is held down
            #if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: # Mouse must be moved to update
                collision = ball.update(ball_speed, walls)
                if collision:
                    # print(collision)
                    ball_rect = ball.getRect()
                    wall_rect = pygame.Rect(collision[0])

                    # """
                    if collision[1] == 0 or collision[1] == 2:
                        ball_speed[1] = -ball_speed[1]
                    if collision[1] == 1 or collision[1] == 3:
                        ball_speed[0] = -ball_speed[0]

                    """
                    if ball_rect.left < wall_rect.right or ball_rect.right > wall_rect.left:
                        ball_speed[0] = -ball_speed[0]
                    if ball_rect.top < wall_rect.bottom or ball_rect.bottom > wall_rect.top:
                        ball_speed[1] = -ball_speed[1]
                    """

        # plain_sprites.update()
        surface_main.blit(background, (0, 0))
        surface_main.blit(foreground, (0, 0))
        plain_sprites.draw(surface_main)
        pygame.display.flip()


if __name__ == "__main__":
    new_layout = getLayout('testMaze')
    print(new_layout)
    main()



