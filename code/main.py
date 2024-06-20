import pygame
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH_screen, HEIGHT_screen))  # seting up the screen
        # setting up the title of the screen
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()  # setting up the clock
        self.level = Level()  # setting up the level, this is where the game will be played

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if the user quits the game, the game will close
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick()/1000
            self.level.run(dt)  # running the level
            if self.level.IfPlayerDied():
                self.level = Level()
            if self.level.newFloor:
                storemoney = self.level.player.money
                storehealth = self.level.player.health
                self.level = Level()
                self.level.player.money = storemoney
                self.level.player.health = storehealth

            pygame.display.update()  # updating the display


if __name__ == '__main__':
    game = Game()
    game.run()
