import os
import pygame


import core.layout as lay

##### VARIABLES #####
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
BG_COLOR = 'black'
DEFAULT_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')


def main():

    pygame.init()

    logo = pygame.image.load(os.path.join(DEFAULT_RESOURCES_DIR, 'test_icon.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    surface_main = pygame.display.set_mode(SCREEN_SIZE)

    # Loading an in
    tst_image  = pygame.image.load(os.path.join(DEFAULT_RESOURCES_DIR, 'intro_ball.gif'))
    ball_speed = [10, 10]
    ball_rect  = tst_image.get_rect()
    # surface_mainMenu = pygame.Surface(SCREEN_SIZE)

    #surface_main.blit(tst_image, (50, 50))
    #pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        ball_rect = ball_rect.move(ball_speed)
        if ball_rect.left < 0 or ball_rect.right > SCREEN_WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball_rect.top < 0 or ball_rect.bottom > SCREEN_HEIGHT:
            ball_speed[1] = -ball_speed[1]

        surface_main.fill(BG_COLOR)
        surface_main.blit(tst_image, ball_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()

    new_layout = lay.getLayout('testMaze')
    print(new_layout)


