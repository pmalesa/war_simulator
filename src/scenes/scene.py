import random

import pygame

from src.models.soldier import Soldier
from src.models.team import TEAM_COLORS, Team


class Scene:
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 1024
    FPS = 60

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._pause = False
        self._max_soldiers = 100
        self._soldiers = self._generate_soldiers()

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

            if self._pause:
                continue

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._pause = not self._pause
                if event.key == pygame.K_r:
                    self._soldiers = self._generate_soldiers()

    def _update(self) -> None:
        for soldier in self._soldiers:
            if (
                soldier.position[0] <= soldier.size
                or soldier.position[0] >= self._width - soldier.size
            ):
                soldier.velocity[0] *= -1
            if (
                soldier.position[1] <= soldier.size
                or soldier.position[1] >= self._height - soldier.size
            ):
                soldier.velocity[1] *= -1

            soldier.move(self._screen)
            soldier.update_nearby_soldiers(self._soldiers)

    def _draw(self) -> None:
        self._screen.fill((30, 30, 30))
        for soldier in self._soldiers:
            soldier.draw(self._screen)

    def _generate_soldiers(
        self,
    ) -> list[Soldier]:
        soldiers = []

        if self._max_soldiers % 2 != 0:
            print("Chosen number of soldiers is not divisible by the number teams.")

        n_soldiers_per_team: int = self._max_soldiers // 2
        id: int = 1

        # Generate GREEN team soldiers
        for i in range(n_soldiers_per_team):
            soldiers.append(
                Soldier(
                    id,
                    f"Soldier_{id}",
                    100,
                    [2, 0],
                    [
                        random.randint(
                            Soldier.DEFAULT_SIZE, (self._width // 2) - Soldier.DEFAULT_SIZE
                        ),
                        random.randint(Soldier.DEFAULT_SIZE, self._height - Soldier.DEFAULT_SIZE),
                    ],
                    1,
                    TEAM_COLORS[Team.GREEN],
                )
            )
            id += 1

        # Generate RED team soldiers
        for i in range(self._max_soldiers - n_soldiers_per_team):
            soldiers.append(
                Soldier(
                    id,
                    f"Soldier_{id}",
                    100,
                    [-2, 0],
                    [
                        random.randint(
                            Soldier.DEFAULT_SIZE + (self._width // 2),
                            self._width - Soldier.DEFAULT_SIZE,
                        ),
                        random.randint(Soldier.DEFAULT_SIZE, self._height - Soldier.DEFAULT_SIZE),
                    ],
                    2,
                    TEAM_COLORS[Team.RED],
                )
            )
            id += 1

        return soldiers
