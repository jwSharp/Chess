# Updated/Created main function that will create window, initialize pygame
# call images, and create instance of scene manager


import pygame
from scene import *

def main():
    # Create Window
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Main Menu")

    BG = pygame.image.load("assets/brainColorful2.jpg")

    # create scene manager
    manager = SceneManager()
    main_menu = MainMenuScene(manager)
    manager.push(main_menu)

    #game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not manager.scenes:
                pygame.quit()
                running = False
            # handle events
            manager.input(event)

        manager.draw(screen)
        pygame.display.update()


main()


