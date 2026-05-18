import random

import pygame

from src.models.soldier import Soldier


class Scene:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    FPS = 60

    def __init__(
        self,
        screen_width: int = DEFAULT_WIDTH,
        screen_height: int = DEFAULT_HEIGHT,
        soldiers: list[Soldier] | None = None,
    ) -> None:
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._running = False
        self._soldiers = soldiers if soldiers is not None else []

        pygame.init()

        # Create window
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
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
            if random.randint(0, 100) < 80:
                soldier.move([-1, -1])
            else:
                soldier.move([1, 1])

    def _draw(self) -> None:
        self._screen.fill((30, 30, 30))
        for soldier in self._soldiers:
            soldier.draw(self._screen)
