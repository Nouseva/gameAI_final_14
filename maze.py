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
    from core import sprite_derived
    # from core.agent import CURRENT_EQUIP

except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)

##### VARIABLES #####
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
WALL_THICKNESS = 20
FPS_CLOCK = None
FPS = 30

BG_COLOR = 'black'
WALL_COLOR = 'white'
GOAL_COLOR = 'yellow'

Item = namedtuple('Item', ['name', 'cost', 'effect', 'slot'])

ACTIVE_LEVEL = None
LOADED_LEVEL = None
MODIFYABLE_LEVEL = None

UNLOCKED_LEVELS = []

EQUIP_PURCHASED = dict()
CURRENT_EQUIP = dict()


COUNTER_WIDGET_ID = 'display_money'
PLAYER_MONEY = 0

ITEM_DICT = None

LEVEL_SELECT = None
EQUIP_STORE = None
EQUIP_MENU = None

GROUP_PLAYER  = pygame.sprite.Group()
GROUP_ENEMIES = pygame.sprite.Group()
GROUP_COINS   = pygame.sprite.Group()

# ITEMS = None
# DEFAULT_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

def load_layout(layout):
    """Loads maze layout onto a pygame surface

    Args:
        layout (core.Layout)
    Returns:
        (walls, agents, loaded_layout)
    """
    global MODIFYABLE_LEVEL
    global GROUP_COINS
    global GROUP_ENEMIES
    global GROUP_PLAYER

    _set_level(0, layout)
    # print(layout)
    MODIFYABLE_LEVEL = layout.deepCopy()

    loaded_layout = pygame.Surface(SCREEN_SIZE)
    walls = []
    boosts = []

    GROUP_PLAYER  = pygame.sprite.Group()
    GROUP_ENEMIES = pygame.sprite.Group()
    GROUP_COINS   = pygame.sprite.Group()


    # print(layout.agentPositions)
    tile_width = SCREEN_WIDTH / layout.width
    tile_height = SCREEN_HEIGHT / layout.height
    # print('before', tile_width, tile_height)
    tile_width, tile_height = utils.nearestPoint((tile_width, tile_height))
    print('after', tile_width, tile_height)

    for wall_tile in layout.walls.asList():
        walls.append(pygame.Rect(wall_tile[0] * tile_width, wall_tile[1] * tile_height, tile_width, tile_height))

    for wall in walls:
        pygame.draw.rect(loaded_layout, WALL_COLOR, wall)

    for coin_pos in layout.food.asList():
        GROUP_COINS.add(sprite_derived.Coin(coin_pos, (tile_width, tile_height)))
    for boost_s in layout.roads.asList():
        boosts.append(sprite_derived.Boost_S(boost_s, (tile_width, tile_height)))
    for boost_l in layout.boost.asList():
        boosts.append(sprite_derived.Boost_L(boost_l, (tile_width, tile_height)))

    gx, gy = layout.getGoal()
    pygame.draw.rect(loaded_layout, GOAL_COLOR, (gx * tile_width, gy * tile_height, tile_width, tile_height))

    for agent in layout.agentPositions:
        # print(agent)
        image = None
        # Player agent
        if agent[0]:
            # image = 'intro_ball.gif'
            image = 'UCSC_slug.png'
        # Enemy agent
        else:
            image = 'enemy.png'

        if agent[0]:
            GROUP_PLAYER.add(Agent(image, CURRENT_EQUIP, (tile_width, tile_height), pos=(agent[1][0], agent[1][1])))
        else:
            GROUP_ENEMIES.add(Agent(image, CURRENT_EQUIP, (tile_width, tile_height), pos = (agent[1][0], agent[1][1]), index = 1))
        # print(agents)


    load_layout = loaded_layout.convert()
    plain_sprites = pygame.sprite.RenderPlain(boosts,)

    return walls, plain_sprites, loaded_layout

"""Functions here handle the creation of all user interfaces
"""
def _start_game(menu):
    global LOADED_LEVEL
    # print(ACTIVE_LEVEL)
    if ACTIVE_LEVEL:
        LOADED_LEVEL = getLayout(ACTIVE_LEVEL)

    menu.disable()
    pass

def _set_level(value, layout_name):
    global ACTIVE_LEVEL
    ACTIVE_LEVEL = layout_name
    # print(ACTIVE_LEVEL)
    pass

def _load_store(menu):
    global EQUIP_STORE
    menu.disable()

    EQUIP_STORE.enable()
    pass

def _load_equip(menu):
    global EQUIP_MENU
    menu.disable()

    EQUIP_MENU.enable()
    pass

def _load_select(menu):
    global LEVEL_SELECT
    menu.disable()

    LEVEL_SELECT.enable()
    pass

def _update_money_display(money_change):
    global PLAYER_MONEY
    PLAYER_MONEY += money_change
    widget = EQUIP_STORE.get_widget(COUNTER_WIDGET_ID)
    new_title = 'MONEY: ' + str(PLAYER_MONEY)
    widget.set_title(new_title)

def _set_equipment(name, cost, descr, slot):#value, item_name):
    global CURRENT_EQUIP
    global EQUIP_PURCHASED

    CURRENT_EQUIP[slot] = EQUIP_PURCHASED[slot][name[1]]
    # print(name, val, desc, slot)
    pass

def _complete_selection(menu):
    global CURRENT_EQUIP

    menu.disable()
    # print(CURRENT_EQUIP)

def _purchase_item(item, menu):
    global PLAYER_MONEY
    global EQUIP_PURCHASED

    global ITEM_DICT
    # print(item)

    # Item has already been purchased
    if item in EQUIP_PURCHASED[item.slot]:
        return

    if PLAYER_MONEY >= item.cost:
        cost = 0 - item.cost
        EQUIP_PURCHASED[item.slot].append(item)
        _update_money_display(cost)
        print(item.name, 'purchased')

        c_button = ITEM_DICT[item]
        # c_button = menu.get_widget(c_index)
        # print(c_button)
        # (c_index.set_background_color((0,255,0))

        new_font = c_button.get_font_info()
        new_font['background_color'] = (100, 150, 100, 255)
        c_button.set_font(new_font['name'], new_font['size'], new_font['color'], new_font['selected_color'], new_font['background_color'])
        c_button.set_background_color(new_font['background_color'])


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
    menu_level.add_button('Equipment', _load_equip, menu_level)
    menu_level.add_button('Store', _load_store, menu_level)
    menu_level.add_button('Quit', pygame_menu.events.EXIT)
    # menu_level.disable()

    LEVEL_SELECT = menu_level
    # return menu_level

def create_equipment_select():
    """ Constructs the menu that allows player to equip their agent (choose heuristics)

    """
    global EQUIP_MENU
    global EQUIP_PURCHASED
    c = 2
    r = 8
    tile_padding = 30
    tile_size = SCREEN_HEIGHT - (tile_padding * (r+1))
    tile_size = tile_size / r

    menu_equip = pygame_menu.Menu(
        SCREEN_HEIGHT, SCREEN_WIDTH, 'Modification Station',
        theme = pygame_menu.themes.THEME_DARK,
        menu_position = (0,0),
        mouse_motion_selection = True,
        enabled = False,
        columns = c, rows = r,
        column_max_width = [SCREEN_WIDTH / c] * c,
        onclose = pygame_menu.events.EXIT,
    )

    menu_equip.add_vertical_margin(tile_size)
    menu_equip.add_button('Level Select', _load_select, menu_equip)
    menu_equip.add_button('Store', _load_store, menu_equip)
    menu_equip.add_vertical_margin(tile_size)
    menu_equip.add_vertical_margin(tile_size)
    menu_equip.add_vertical_margin(tile_size)
    menu_equip.add_vertical_margin(tile_size)
    menu_equip.add_vertical_margin(tile_size)

    for slot, gear_list in EQUIP_PURCHASED.items():
        menu_equip.add_selector(
            title = slot,
            items = gear_list,
            onchange = _set_equipment,
        )


    EQUIP_MENU = menu_equip
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
    r = 8
    c = 4

    menu_shop = pygame_menu.Menu(
        SCREEN_HEIGHT, SCREEN_WIDTH, 'Item Shop',
        theme   = pygame_menu.themes.THEME_DARK,
        columns = c,
        rows    = r,
        enabled = False,
        onclose = pygame_menu.events.EXIT,
        center_content = False,
        column_max_width = [SCREEN_WIDTH / c] * c,
        # menu_position = (0, 0),
        mouse_motion_selection = True,
        )
    tile_padding = 30
    tile_size = SCREEN_HEIGHT - (tile_padding * (r+1))
    tile_size = tile_size / r
    current_money = 'MONEY: ' + str(PLAYER_MONEY)
    menu_shop.add_label(
        title = current_money,
        align = pygame_menu.locals.ALIGN_LEFT,
        label_id = COUNTER_WIDGET_ID,
        margin = (tile_padding, tile_padding)

    )

    menu_shop.add_button(
        'Level Select', _load_select, menu_shop,
        align = pygame_menu.locals.ALIGN_CENTER,
        margin = (0, tile_padding)
    )

    menu_shop.add_button(
        'Equipment', _load_equip, menu_shop,
        align = pygame_menu.locals.ALIGN_CENTER,
        margin = (0, tile_padding)
    )

    menu_shop.add_vertical_margin(tile_size)
    menu_shop.add_vertical_margin(tile_size)
    menu_shop.add_vertical_margin(tile_size)
    menu_shop.add_vertical_margin(tile_size)
    menu_shop.add_vertical_margin(tile_size)

    row = 0
    for item in item_list:
        row = row % menu_shop._rows
        if row == 0:
            menu_shop.add_vertical_margin(tile_size)
            row += 1

        c_button = menu_shop.add_button(
            item.name, _purchase_item, item, menu_shop,
            margin = (tile_padding, tile_padding),
        )
        ITEM_DICT[item] = c_button
        row += 1

    # TODO: ADD MONEY DISPLAY, VISUAL INDICATION OF PURCHASE
    # menu_shop.add_vertical_margin(200)

    EQUIP_STORE = menu_shop
    EQUIP_STORE.disable()
    # return menu_shop

def goto_level_select(surface, maze_layouts):
    global ACTIVE_LEVEL
    global LEVEL_SELECT

    results = None

    # TODO: Fix bug where ACTIVE_LEVEL does not match selector after first call
    ACTIVE_LEVEL = maze_layouts[0][1]
    while LEVEL_SELECT.is_enabled():
        FPS_CLOCK.tick(FPS)

        events = pygame.event.get()

        LEVEL_SELECT.draw(surface)
        LEVEL_SELECT.update(events)

        pygame.display.update()

    if LOADED_LEVEL:
        results = load_layout(LOADED_LEVEL)

        # results = results[0], plain_sprites, results[2]

    return results

def goto_equip_store(surface):
    global EQUIP_STORE
    global PLAYER_MONEY

    _update_money_display(FPS)

    while EQUIP_STORE.is_enabled():
        FPS_CLOCK.tick(30)

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.KEYDOWN:
                change = 0
                if event.key == K_0:
                    change -= PLAYER_MONEY
                elif event.key == K_m:
                    change += 1000
                elif event.key == K_MINUS:
                    change -= 1000
                _update_money_display(change)

        EQUIP_STORE.draw(surface)
        EQUIP_STORE.update(events)

        pygame.display.update()
    # print(EQUIP_PURCHASED)
    pass

def goto_equip_screen(surface):
    global EQUIP_MENU

    while EQUIP_MENU.is_enabled():
        FPS_CLOCK.tick(FPS)

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
    global LOADED_LEVEL
    global MODIFYABLE_LEVEL

    global FPS_CLOCK
    global UNLOCKED_LEVELS

    # TODO: Levels unlock in some manner
    UNLOCKED_LEVELS = maze_layouts

    pygame.init()
    surface_main = pygame.display.set_mode(SCREEN_SIZE)

    # logo, _ = utils.load_image('test_icon.png', scale = (64, 64))
    logo, _ = utils.load_image('UCSC_slug.png', scale = (64, 64))
    pygame.display.set_icon(logo)
    pygame.display.set_caption('UCSC CMPS 140 Final')

    background = pygame.Surface(surface_main.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    foreground = None
    plain_sprites = None
    agents = None

    create_level_select(maze_layouts)

    create_equipment_shop(ITEMS)
    create_equipment_select()

    LEVEL_SELECT.enable()

    FPS_CLOCK = pygame.time.Clock()
    while 1:
        # Framerate controller
        FPS_CLOCK.tick(FPS)
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
                for sprite in GROUP_PLAYER:
                    lvl_complete = sprite.update(CURRENT_EQUIP, MODIFYABLE_LEVEL, GROUP_ENEMIES, GROUP_COINS)
                    if lvl_complete:
                        # Value can be changed to be dependent on score of player
                        # print(lvl_complete)
                        _update_money_display(lvl_complete)
                        foreground = None
                        plain_sprites = []
                        # surface_main.blit(foreground, (0, 0))
                        # surface_main.blit(background, (0, 0))
                        LEVEL_SELECT.enable()
                        LOADED_LEVEL = None
                for sprite in GROUP_ENEMIES:
                    sprite.update(None, MODIFYABLE_LEVEL, GROUP_PLAYER, None)



        surface_main.blit(background, (0, 0))
        if LEVEL_SELECT.is_enabled():
            results = goto_level_select(surface_main, UNLOCKED_LEVELS)
            if results:
                walls, plain_sprites, foreground = results
        if EQUIP_STORE.is_enabled():
            goto_equip_store(surface_main)
        if EQUIP_MENU.is_enabled():
            goto_equip_screen(surface_main)

        # plain_sprites.update()
        if foreground:
            surface_main.blit(foreground, (0, 0))
        if plain_sprites:
            plain_sprites.draw(surface_main)
        GROUP_COINS.draw(surface_main)
        GROUP_ENEMIES.draw(surface_main)
        GROUP_PLAYER.draw(surface_main)
        pygame.display.flip()


if __name__ == "__main__":

    layouts = [
        ('Test Maze', 'testMaze'),
        ('Easy Maze', 'mediumClassic'),
        ('Level 01' , 'map_1'),
        ('Level 02' , 'map_2'),
        ('Level 03' , 'map_3'),
        ('Level 04' , 'map_4'),
        ('Demo Maze' , 'demo_map'),
    ]

    global ITEMS
    # Items is a list of namedtuple Item()
    ITEMS = [
        Item('Goggles', 30, 'Googly Goggles', 'helmet'),
        Item('Wheels', 10, 'Wheely fast', 'legs'),
        Item('Backpack', 20, 'Soft sack', 'torso'),
        Item('Claws', 10, 'Spiky', 'arms'),
        Item('Some Junk', 999, 'Useless', 'trinket'),
        Item('Magguffin 5000', 4999, 'One to rule them all', 'trinket'),
    ]

    EQUIP_PURCHASED['helmet']  = [Item('', 0, '', 'helmet')]
    EQUIP_PURCHASED['legs']    = [Item('', 0, '', 'legs')]
    EQUIP_PURCHASED['torso']   = [Item('', 0, '', 'torso')]
    EQUIP_PURCHASED['arms']    = [Item('', 0, '', 'arms')]
    EQUIP_PURCHASED['trinket'] = [Item('', 0, '', 'trinket')]

    CURRENT_EQUIP['helmet']  = EQUIP_PURCHASED['helmet'][0]
    CURRENT_EQUIP['legs']    = EQUIP_PURCHASED['legs'][0]
    CURRENT_EQUIP['torso']   = EQUIP_PURCHASED['torso'][0]
    CURRENT_EQUIP['arms']    = EQUIP_PURCHASED['arms'][0]
    CURRENT_EQUIP['trinket'] = EQUIP_PURCHASED['trinket'][0]


    # layouts_dict = { layout_name: getLayout(layout_name) for layout_name, display_name in layouts }

    # print(layouts)
    main(layouts)
