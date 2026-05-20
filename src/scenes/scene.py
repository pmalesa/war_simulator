import random

import pygame

from src.models.soldier import Soldier


class Scene:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    FPS = 60

    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        soldiers: list[Soldier] | None = None,
    ) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._soldiers = soldiers if soldiers is not None else []

        pygame.init()

        # Create window
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("War simulator")

        self._clock = pygame.time.Clock()

        print("Scene initialized.")

    def run(self):
        self._running = True

        while self._running:
            self._handle_events()
            self._update()
            self._draw()

            # Update display
            pygame.display.flip()
            self._clock.tick(self.FPS)

        # Cleanup
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _update(self) -> None:
        for soldier in self._soldiers:
            direction = [1, 1]

            if soldier.position[0] <= soldier.size:
                direction[0] = 1
            elif soldier.position[0] >= self._width - soldier.size:
                direction[0] = -1

            if soldier.position[1] <= soldier.size:
                direction[1] = 1
            elif soldier.position[1] >= self._height - soldier.size:
                direction[1] = -1

            nearby_soldiers = soldier.get_nearby_soldiers(self._soldiers)

            if nearby_soldiers:
                soldier.position = [
                    random.randint(soldier.size, self._width),
                    random.randint(soldier.size, self._height),
                ]

            soldier.move(self._screen, direction)

    def _draw(self) -> None:
        self._screen.fill((30, 30, 30))
        for soldier in self._soldiers:
            soldier.draw(self._screen)
