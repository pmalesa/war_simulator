import random
import sys

import pygame

from src.models.soldier import Soldier


class Scene:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(
        self,
        screen_width: int = DEFAULT_WIDTH,
        screen_height: int = DEFAULT_HEIGHT,
        soldiers: list[Soldier] = [],
    ):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._running = False
        self._soldiers = soldiers

        pygame.init()

        # Create window
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("War simulator")

        print("Scene initialized.")

    def run(self):
        self._running = True
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # Background color
            self._screen.fill((30, 30, 30))

            # Draw soldiers
            for soldier in self._soldiers:
                if random.randint(0, 100) < 80:
                    soldier.move([-1, -1])
                else:
                    soldier.move([1, 1])
                pygame.draw.circle(self._screen, soldier.color, soldier.position, soldier.size)

            # Update display
            pygame.display.flip()

        # Cleanup
        pygame.quit()
        sys.exit()
