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

def load_layout(layout):
    """Loads maze layout onto a pygame surface
    """

    loaded_layout = pygame.Surface(SCREEN_SIZE)
    walls = []
    agents = []

    # print(layout.agentPositions)
    tile_width = SCREEN_WIDTH / layout.width
    tile_height = SCREEN_HEIGHT / layout.height
    
    for wall_tile in layout.walls.asList():
        walls.append(pygame.Rect(wall_tile[0] * tile_width, wall_tile[1] * tile_height, tile_width, tile_height))

    for wall in walls:
        pygame.draw.rect(loaded_layout, WALL_COLOR, wall)
    
    for agent in layout.agentPositions:
        image = None
        # Player agent
        if agent[0]:
            image = 'intro_ball.gif'
        # Enemy agent
        else:
            image = 'test_icon.png'

        agents.append(Agent(image, pos=(tile_width * agent[1][0], tile_height * agent[1][1])))
        # print(agents)



    load_layout = loaded_layout.convert()

    return walls, agents, loaded_layout


def main(maze_layout):
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

    """
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
    """

    walls, agents, foreground = load_layout(maze_layout)

    # Loading an in
    # ball_image, ball_rect  = utils.load_image('intro_ball.gif')

    ball_speed = [5, 5]
    # surface_mainMenu = pygame.Surface(SCREEN_SIZE)

    #surface_main.blit(ball_image, (50, 50))
    #pygame.display.flip()

    plain_sprites = pygame.sprite.RenderPlain(agents)
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
                for sprite in plain_sprites:
                    collision = sprite.update(ball_speed, walls)
                    if collision != -1:
                        # print(collision)
                        ball_rect = sprite.getRect()
                        wall_rect = walls[collision]
                        # wall_rect = pygame.Rect(collision)

                        """
                        if collision[1] == 0 or collision[1] == 2:
                            ball_speed[1] = -ball_speed[1]
                        if collision[1] == 1 or collision[1] == 3:
                            ball_speed[0] = -ball_speed[0]

                        """
                        if ball_rect.left < wall_rect.right or ball_rect.right > wall_rect.left:
                            ball_speed[0] = -ball_speed[0]
                        if ball_rect.top < wall_rect.bottom or ball_rect.bottom > wall_rect.top:
                            ball_speed[1] = -ball_speed[1]
                        # """

        # plain_sprites.update()
        surface_main.blit(background, (0, 0))
        surface_main.blit(foreground, (0, 0))
        plain_sprites.draw(surface_main)
        pygame.display.flip()


if __name__ == "__main__":
    # new_layout = getLayout('testMaze')
    new_layout = getLayout('mediumClassic')
    print(new_layout)
    main(new_layout)



