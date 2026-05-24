import random

import pygame

from src.models.soldier import Soldier


class Scene:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    FPS = 60

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._soldiers = self._generate_soldiers(100, 10)

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

    def _generate_soldiers(self, n_soldiers: int, n_teams: int = 2) -> list[Soldier]:
        soldiers = []

        if n_soldiers % n_teams != 0:
            print("Chosen number of soldiers is not divisible by the number teams.")

        n_soldiers_per_team: int = n_soldiers // n_teams
        n_soldiers_left: int = n_soldiers % n_teams
        id: int = 1

        for team in range(n_teams):
            team_color: tuple[int] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

            for i in range(n_soldiers_per_team):
                soldiers.append(
                    Soldier(
                        id,
                        f"Soldier_{id}",
                        100,
                        [2, 2],
                        [
                            random.randint(
                                Soldier.DEFAULT_SIZE, self._width - Soldier.DEFAULT_SIZE
                            ),
                            random.randint(
                                Soldier.DEFAULT_SIZE, self._height - Soldier.DEFAULT_SIZE
                            ),
                        ],
                        team + 1,
                        team_color,
                    )
                )

            if n_soldiers_left > 0:
                id += 1
                n_soldiers_left -= 1
                soldiers.append(
                    Soldier(
                        id,
                        f"Soldier_{id}",
                        100,
                        [2, 2],
                        [
                            random.randint(
                                Soldier.DEFAULT_SIZE, self._width - Soldier.DEFAULT_SIZE
                            ),
                            random.randint(
                                Soldier.DEFAULT_SIZE, self._height - Soldier.DEFAULT_SIZE
                            ),
                        ],
                        team + 1,
                        team_color,
                    )
                )

        return soldiers
