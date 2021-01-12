import pygame
import random


pygame.init()
class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.clock()
        


    def play_step(self):
        pass


if __name__ == "__main__":
    game = SnakeGame()

    # main loop
    while True:
        game.play_step()

        if game_over:
            break


    pygame.quit()
