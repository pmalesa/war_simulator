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
                self.__move_soldier_randomly(soldier)
                pygame.draw.circle(self._screen, soldier.color, soldier.position, soldier.size)

            # Update display
            pygame.display.flip()

        # Cleanup
        pygame.quit()
        sys.exit()

    def __move_soldier_randomly(self, soldier: Soldier):
        val_x: int = random.randint(-1, 1)
        val_y: int = random.randint(-1, 1)
        new_x: int = soldier.position[0] + val_x
        new_y: int = soldier.position[1] + val_y
        soldier.position = (
            self.__clamp(new_x, self._screen_width),
            self.__clamp(new_y, self._screen_height),
        )

    def __clamp(self, x: int, max_val: int) -> int:
        return min(max(0, x), max_val)
