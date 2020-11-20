import pygame
import os

import core.layout as lay

##### VARIABLES #####
screen_width    = 1200
screen_height   = 600

def main():

    pygame.init()

    logo = pygame.image.load("resources/test_icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    pygame.display.set_mode((screen_width, screen_height))

    # Loading an in
    tst_image = pygame.image.load('resources/test_icon.png')
    surface_mainMenu = pygame.Surface((screen_width, screen_height))

    surface_mainMenu.blit(tst_image, (50, 50))
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    #main()

    new_layout = lay.getLayout('testMaze')
    print(new_layout)


