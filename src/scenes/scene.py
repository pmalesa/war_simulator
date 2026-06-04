import random

import pygame
from pygame import Rect

from src.models.soldier import Soldier
from src.models.team import TEAM_COLORS, Team


class Scene:
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 1024
    WALL_COUNT = 10
    WALL_COLOR = (150, 150, 150)
    FPS = 60

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._pause = False
        self._max_soldiers = 200
        self._soldiers = self._generate_soldiers()
        self._obstacles = self._generate_obstacles(Scene.WALL_COUNT)

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
                    self._obstacles = self._generate_obstacles(Scene.WALL_COUNT)

    def _update(self) -> None:
        for soldier in self._soldiers:
            soldier.move(self._screen, self._obstacles)
            soldier.update_nearby_soldiers(self._soldiers)
            soldier.update_visible_soldiers(self._soldiers)

    def _draw(self) -> None:
        self._screen.fill((30, 30, 30))

        for obstacle in self._obstacles:
            pygame.draw.rect(self._screen, Scene.WALL_COLOR, obstacle)

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

    def _generate_obstacles(self, count: int) -> list[Rect]:
        obstacles = []

        for _ in range(count):
            if random.randint(0, 100) < 50:
                width = random.randint(80, 180)
                height = random.randint(15, 20)
            else:
                width = random.randint(15, 20)
                height = random.randint(80, 180)

            x = random.randint(0, self._width - width)
            y = random.randint(0, self._height - height)

            obstacle = Rect(x, y, width, height)
            obstacles.append(obstacle)

        return obstacles
