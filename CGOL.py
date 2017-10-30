import pygame
import config_loader
from Classes import *


def main():
    configs = config_loader.ConfigEditor()
    videoSettings = configs.video_config_load()
    fsflags = False
    if videoSettings["fullscreen"] == True:
        fsflags = pygame.FULLSCREEN | pygame.HWSURFACE
    else:
        fsflags = False
    screen = pygame.display.set_mode(videoSettings["resolution"], fsflags)
    # Game loop constants
    clock = pygame.time.Clock()
    gameRunning = True

    display = Display()
    while gameRunning:
        clock.tick(600)
        screen.fill([0,0,0])
        events = pygame.event.get()
        display.update()
        display.render(screen)
        display.handle_Events(events)
        for event in events:
            if event.type == pygame.QUIT:
                gameRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameRunning = False

        pygame.display.flip()


if __name__ == "__main__":
    main()
