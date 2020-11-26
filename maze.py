#!/usr/bin/env python

try:
    import sys
    import os
    import pygame
    import pygame_menu

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

ACTIVE_LEVEL = None
LOADED_LEVEL = None
# DEFAULT_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

def load_layout(layout):
    """Loads maze layout onto a pygame surface

    Args:
        layout (core.Layout):
    """

    _set_level(0, layout)

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

"""Functions here handle the creation of all user interfaces
"""
def _start_game(menu):
    global LOADED_LEVEL
    if ACTIVE_LEVEL:
        LOADED_LEVEL = getLayout(ACTIVE_LEVEL)
        menu.toggle()
    pass

def _set_level(value, layout_name):
    global ACTIVE_LEVEL
    ACTIVE_LEVEL = layout_name
    print(ACTIVE_LEVEL)
    pass

def level_select(level_list):
    """ Creates menu that allows player to select a level (layout) from the available options

    Args:
        screen_size: (screen_width, screen_height)
        level_list: list of tuples (display_name, index_of_level_layout)

    """
    menu_level = pygame_menu.Menu(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 'Level Select', theme = pygame_menu.themes.THEME_DARK)
    menu_level.add_selector('Level :', level_list, onchange = _set_level)
    menu_level.add_button('Play', _start_game, menu_level)
    menu_level.add_button('Quit', pygame_menu.events.EXIT)

    return menu_level

def augment_store():
    pass

def augment_config():
    pass

def main(maze_layouts):
    global ACTIVE_LEVEL
    ACTIVE_LEVEL = maze_layouts[0][1]

    pygame.init()
    # pygame.display.init()
    # pygame.mixer.quit() # Disable sound
    # print(pygame.mixer.get_init())
    surface_main = pygame.display.set_mode(SCREEN_SIZE)

    logo, _ = utils.load_image('test_icon.png', -1)
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    background = pygame.Surface(surface_main.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    level_select_menu = level_select(maze_layouts)

    # TODO: Fix menu display
    level_select_menu.mainloop(surface_main)


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

    walls, agents, foreground = load_layout(LOADED_LEVEL)

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
        events = pygame.event.get()

        for event in events:
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

        if level_select_menu.is_enabled():
            level_select_menu.update(events)
            level_select_menu.draw(surface_main)

        # plain_sprites.update()
        surface_main.blit(background, (0, 0))
        surface_main.blit(foreground, (0, 0))
        plain_sprites.draw(surface_main)
        pygame.display.flip()


if __name__ == "__main__":
    """
    # new_layout = getLayout('testMaze')
    new_layout = getLayout('mediumClassic')
    print(new_layout)
    main(new_layout)
    """

    layouts = [
        ('Test Maze', 'testMaze'),
        ('Easy Maze', 'mediumClassic'),
    ]

    # layouts_dict = { layout_name: getLayout(layout_name) for layout_name, display_name in layouts }

    # print(layouts_dict)
    main(layouts)



