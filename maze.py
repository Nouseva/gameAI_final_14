#!/usr/bin/env python

try:
    import sys
    import os
    import pygame
    import pygame_menu

    from pygame.locals import *
    from collections import namedtuple
    from itertools import chain

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
surface_main = None

Item = namedtuple('Item', ['name', 'cost', 'effect', 'slot'])

ACTIVE_LEVEL = None
LOADED_LEVEL = None
EQUIP_PURCHASED = dict()
CURRENT_EQUIP = dict()
PLAYER_MONEY = 0

# ITEMS = None
ITEM_DICT = None

LEVEL_SELECT = None
EQUIP_STORE = None
EQUIP_MENU = None

# ITEMS = None
# DEFAULT_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

def load_layout(layout):
    """Loads maze layout onto a pygame surface

    Args:
        layout (core.Layout):
    """

    _set_level(0, layout)
    print(layout)

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
    print(ACTIVE_LEVEL)
    if ACTIVE_LEVEL:
        LOADED_LEVEL = getLayout(ACTIVE_LEVEL)

    menu.disable()
    pass

def _set_level(value, layout_name):
    global ACTIVE_LEVEL
    ACTIVE_LEVEL = layout_name
    # print(ACTIVE_LEVEL)
    pass

def create_level_select(level_list):
    """ Creates menu that allows player to select a level (layout) from the available options

    Args:
        screen_size: (screen_width, screen_height)
        level_list: list of tuples (display_name, index_of_level_layout)

    """
    # Necessary to modify glob var
    global LEVEL_SELECT

    menu_level = pygame_menu.Menu(
        SCREEN_HEIGHT, SCREEN_WIDTH/3, 'Level Select',
        theme = pygame_menu.themes.THEME_DARK,
        menu_position = (0, 0),
        mouse_motion_selection = True,
        enabled = False,
        onclose = pygame_menu.events.EXIT,
        )
    menu_level.add_selector('Level :', level_list, onchange = _set_level)
    menu_level.add_button('Play', _start_game, menu_level)
    menu_level.add_button('Quit', pygame_menu.events.EXIT)
    # menu_level.disable()

    LEVEL_SELECT = menu_level
    # return menu_level

def _set_equipment(name, cost, descr, slot):#value, item_name):
    global CURRENT_EQUIP
    global EQUIP_PURCHASED

    CURRENT_EQUIP[slot] = EQUIP_PURCHASED[slot][name[1]]
    # print(name, val, desc, slot)
    pass

def _complete_selection(menu):
    global CURRENT_EQUIP

    menu.disable()
    print(CURRENT_EQUIP)

def create_equipment_select():
    """ Constructs the menu that allows player to equip their agent (choose heuristics)
    
    """
    global EQUIP_MENU
    global EQUIP_PURCHASED

    menu_equip = pygame_menu.Menu(
        SCREEN_HEIGHT, SCREEN_WIDTH, 'Modification Station',
        theme = pygame_menu.themes.THEME_DARK,
        menu_position = (0,0),
        mouse_motion_selection = True,
        enabled = False,
        onclose = pygame_menu.events.EXIT,
    )

    for slot, gear_list in EQUIP_PURCHASED.items():
        menu_equip.add_selector(
            title = slot,
            items = gear_list,
            onchange = _set_equipment,
        )

    menu_equip.add_button('Play', _complete_selection, menu_equip)
    EQUIP_MENU = menu_equip
    pass

def _purchase_item(item):
    global PLAYER_MONEY
    global EQUIP_PURCHASED
    print(item)

    # Item has already been purchased
    if item in EQUIP_PURCHASED[item.slot]:
        return

    if PLAYER_MONEY >= item.cost:
        PLAYER_MONEY -= item.cost
        EQUIP_PURCHASED[item.slot].append(item)
        print(item.name, 'purchased')

    pass

def _complete_purchases ():
    global EQUIP_MENU
    global EQUIP_STORE

    EQUIP_MENU.enable()
    EQUIP_STORE.disable()
    pass

def create_equipment_shop(item_list):
    """ Menu that allows player to purchase the equipment that will be available to them.
    (The heuristic options that can be chosen/modified) 

    Args:
        item_list: Items that will be sold to the player (display_name, index_of_item)

    # TODO: Look at widgets.core.Selection for selection information display

    """
    global EQUIP_STORE
    global ITEM_DICT
    ITEM_DICT = dict()

    menu_shop = pygame_menu.Menu(
        SCREEN_HEIGHT, SCREEN_WIDTH, 'Item Shop',
        theme   = pygame_menu.themes.THEME_DARK,
        columns = 7,
        rows    = 3,
        enabled = False,
        onclose = pygame_menu.events.EXIT,
        center_content = False,
        # menu_position = (0, 0),
        # mouse_motion_selection = True,
        )
    tile_padding = 30
    tile_size = SCREEN_WIDTH - (tile_padding * len(item_list))
    tile_size = tile_size / len(item_list)
    for item in item_list:
        menu_shop.add_button(item.name, _purchase_item, item)
        c_menu = menu_shop.get_index()
        ITEM_DICT[c_menu] = item

    menu_shop.add_vertical_margin(200)

    menu_shop.add_button(
        title = 'Equip Bot',
        action = _complete_purchases,
        align = pygame_menu.locals.ALIGN_CENTER,

        )
    EQUIP_STORE = menu_shop
    EQUIP_STORE.disable()
    # return menu_shop

def goto_level_select(surface, maze_layouts):
    global ACTIVE_LEVEL
    global LEVEL_SELECT

    # TODO: Fix bug where ACTIVE_LEVEL does not match selector after first call
    ACTIVE_LEVEL = maze_layouts[0][1]
    # LEVEL_SELECT.enable()
    # print('level_select active')
    while LEVEL_SELECT.is_enabled():
        events = pygame.event.get()

        LEVEL_SELECT.draw(surface)
        LEVEL_SELECT.update(events)

        pygame.display.update()
    # LEVEL_SELECT.mainloop(surface)
    # LEVEL_SELECT.disable()
    # print('level_select inactive')
    walls, agents, foreground = load_layout(LOADED_LEVEL)
    plain_sprites = pygame.sprite.RenderPlain(agents)

    return walls, plain_sprites, foreground

def goto_equip_store(surface):
    global EQUIP_STORE
    global PLAYER_MONEY

    # EQUIP_STORE.enable()
    while EQUIP_STORE.is_enabled():
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == K_0:
                    PLAYER_MONEY = 0
                    print(PLAYER_MONEY)
                elif event.key == K_PLUS:
                    PLAYER_MONEY += 1000
                    print(PLAYER_MONEY)
                elif event.key == K_MINUS:
                    PLAYER_MONEY -= 1000
                    print(PLAYER_MONEY)

        EQUIP_STORE.draw(surface)
        EQUIP_STORE.update(events)
            

        

        pygame.display.update()
    # EQUIP_STORE.get_selected_widget().get_title()
    print(EQUIP_PURCHASED)
    pass

def goto_equip_screen(surface):
    global EQUIP_MENU

    # EQUIP_MENU.enable()
    while EQUIP_MENU.is_enabled():
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.KEYDOWN:
                pass

        EQUIP_MENU.draw(surface)
        EQUIP_MENU.update(events)

        pygame.display.update()

    pass

def main(maze_layouts):
    global ACTIVE_LEVEL
    global surface_main
    # ACTIVE_LEVEL = maze_layouts[0][1]

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

    create_level_select(maze_layouts)
    
    create_equipment_shop(ITEMS)
    create_equipment_select()

    # TODO: Fix menu display
    # level_select_menu.mainloop(surface_main)
    LEVEL_SELECT.enable()
    # walls, plain_sprites, foreground = goto_level_select(surface_main, maze_layouts)


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

    # walls, agents, foreground = load_layout(LOADED_LEVEL)

    ball_speed = [5, 5]

    # plain_sprites = pygame.sprite.RenderPlain(agents)
    clock = pygame.time.Clock()

    while 1:
        # Framerate controller
        clock.tick(30)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                # List of keys that are active
                # keys = [ i for i, v in enumerate(pygame.key.get_pressed()) if v ]
                # for key in keys:

                # key 'l' (lower L) enables level select menu
                if event.key == pygame.K_l:
                    LEVEL_SELECT.enable()
                    # walls, plain_sprites, foreground = goto_level_select(surface_main, maze_layouts)
                    # ACTIVE_LEVEL = maze_layouts[0][1]
                    # level_select_menu.toggle()
                    # level_select_menu.mainloop(surface_main)
                    # walls, agents, foreground = load_layout(LOADED_LEVEL)
                    # plain_sprites = pygame.sprite.RenderPlain(agents)
                # key 'p' enables store menu
                elif event.key == pygame.K_p:
                    EQUIP_STORE.enable()
                    # goto_equip_store(surface_main)
                    # equip_shop_menu.toggle()
                    # equip_shop_menu.mainloop(surface_main)
                    pass

                # key 'i' enables equipment menu
                elif event.key == pygame.K_i:
                    EQUIP_MENU.enable()
                    pass
            
            # Ball will only move when the mouse button is held down
            elif event.type == pygame.MOUSEBUTTONDOWN:
            # if pygame.mouse.get_pressed()[0]: # Mouse must be moved to update
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

        if LEVEL_SELECT.is_enabled():
            walls, plain_sprites, foreground = goto_level_select(surface_main, maze_layouts)
        if EQUIP_STORE.is_enabled():
            goto_equip_store(surface_main)
        if EQUIP_MENU.is_enabled():
            print('hellp')
            goto_equip_screen(surface_main)

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

    global ITEMS
    # Items is a list of namedtuple Item()
    ITEMS = [
        Item('Wheels', 10, 'Wheely fast', 'legs'),
        Item('Backpack', 20, 'Soft sack', 'torso'),
        Item('Claws', 10, 'Spiky', 'arms'),
        Item('Some Junk', 999, 'Useless', 'trinket'),
        Item('Magguffin 5000', 4999, 'One to rule them all', 'trinket'),
    ]

    EQUIP_PURCHASED['legs'] = [Item('', 0, '', 'legs')]
    EQUIP_PURCHASED['torso'] = [Item('', 0, '', 'torso')]
    EQUIP_PURCHASED['arms'] = [Item('', 0, '', 'arms')]
    EQUIP_PURCHASED['trinket'] = [Item('', 0, '', 'trinket')]
    CURRENT_EQUIP['legs'] = EQUIP_PURCHASED['legs'][0]
    CURRENT_EQUIP['torso'] = EQUIP_PURCHASED['torso'][0]
    CURRENT_EQUIP['arms'] = EQUIP_PURCHASED['arms'][0]
    CURRENT_EQUIP['trinket'] = EQUIP_PURCHASED['trinket'][0]


    # layouts_dict = { layout_name: getLayout(layout_name) for layout_name, display_name in layouts }

    print(layouts)
    main(layouts)



