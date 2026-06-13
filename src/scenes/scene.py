import math
import random

import pygame

from src.models.soldier import Soldier
from src.models.team import TEAM_COLORS, Team
from src.models.wall import Wall


class Scene:
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 1024
    WALL_COUNT = 20
    MAX_SOLDIERS = 200
    FPS = 60

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._pause = False
        self._max_soldiers = Scene.MAX_SOLDIERS
        self._soldiers: list[Soldier] = self._generate_soldiers()
        self._walls: list[Wall] = self._generate_walls(Scene.WALL_COUNT)

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
                    self._walls = self._generate_walls(Scene.WALL_COUNT)

    def _update(self) -> None:
        for soldier in self._soldiers:
            soldier.update(self._screen, self._walls)
            soldier.update_nearby_soldiers(self._soldiers)
            soldier.update_visible_soldiers(self._soldiers)

    def _draw(self) -> None:
        self._screen.fill((30, 30, 30))

        for wall in self._walls:
            wall.draw(self._screen)

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

    def _generate_walls(self, n_walls: int) -> list[Wall]:
        walls: list[Wall] = []

        # Divide the scene into n_walls regions
        n_rows = math.ceil(math.sqrt(n_walls))
        n_cols = math.ceil(n_walls / n_rows)
        n_regions = n_rows * n_cols

        region_w = self._width / n_cols
        region_h = self._height / n_rows
        all_regions: list[tuple[float, float]] = [
            ((i % n_cols) * region_w, (i // n_cols) * region_h) for i in range(n_regions)
        ]

        # Randomly select only n_walls regions
        selected_regions: list[tuple[float, float]] = random.sample(all_regions, n_walls)

        # Generate walls in selected regions
        long_side_range: tuple[int, int] = (80, 160)
        short_side_range: tuple[int, int] = (15, 20)
        for selected_region in selected_regions:
            region_x, region_y = selected_region
            is_horizontal: bool = random.choice([True, False])
            if is_horizontal:
                wall_w = random.randint(*long_side_range)
                wall_h = random.randint(*short_side_range)
            else:
                wall_w = random.randint(*short_side_range)
                wall_h = random.randint(*long_side_range)

            wall_x = random.uniform(region_x, region_x + region_w - wall_w)
            wall_y = random.uniform(region_y, region_y + region_h - wall_h)

            # Cap the wall size to region size
            wall_w = min(wall_w, region_w)
            wall_h = min(wall_h, region_h)

            wall = Wall(wall_x, wall_y, wall_w, wall_h)
            walls.append(wall)

        return walls
