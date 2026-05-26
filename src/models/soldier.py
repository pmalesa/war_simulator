import math
import random

import pygame
from pygame import Surface


class Soldier:
    MAX_HEALTH: int = 100
    DEFAULT_STEP: int = 1
    DEFAULT_SIZE: int = 10
    DEFAULT_AWARENESS_RADIUS = 10
    DEFAULT_FIELD_OF_VIEW_ANGLE = 30

    def __init__(
        self,
        id: int,
        name: str,
        health: int = MAX_HEALTH,
        velocity: list[float] | None = None,
        position: list[float] | None = None,
        team: int = 1,
        color: tuple[int] | None = None,
        size: int = DEFAULT_SIZE,
        step: int = DEFAULT_STEP,
        awareness_radius: int = DEFAULT_AWARENESS_RADIUS,
        field_of_view_angle: int = DEFAULT_FIELD_OF_VIEW_ANGLE,
        nearby_soldiers: list["Soldier"] | None = None,
    ):
        self.id = id
        self.name = name
        self.health = health

        self.velocity = velocity if velocity is not None else [1, 1]
        self.position = position if position is not None else [0, 0]
        self.direction = None
        self.face_direction: list[int] = [0, 0]

        self.color = color if color is not None else (255, 0, 0)
        self.team = team

        self.size = size
        self.step = step

        self.awareness_radius = awareness_radius
        self.field_of_view_angle = field_of_view_angle

        self.nearby_soldiers = nearby_soldiers if nearby_soldiers is not None else []

    def shoot(self) -> None:
        pass

    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        return self.health > 0

    def move(self, screen: Surface) -> None:
        if not self.velocity:
            return

        self.direction = self._get_direction()
        self.position[0] += self.velocity[0] * self.step
        self.position[1] += self.velocity[1] * self.step

        self.position[0] = max(0, min(self.position[0], screen.get_width() - self.size))
        self.position[1] = max(0, min(self.position[1], screen.get_height() - self.size))

        for nearby_soldier in self.nearby_soldiers:
            if nearby_soldier.team != self.team:
                self.health = max(0, self.health - 20)

                self.velocity[0] *= -1
                self.velocity[1] *= -1

                if not self.is_alive():
                    self.position = [
                        random.randint(self.size, screen.get_width() - self.size),
                        random.randint(self.size, screen.get_height() - self.size),
                    ]

    def draw(self, screen: Surface) -> None:
        if not isinstance(screen, Surface) or not screen:
            raise RuntimeError(
                f"Invalid type of screen object: {type(screen)} instead of pygame.Surface."
            )
        pygame.draw.circle(screen, self.color, self.position, self.size)
        self._draw_direction_line(screen)

    def update_nearby_soldiers(self, soldiers: list["Soldier"]) -> None:
        self.nearby_soldiers = []

        radius_squared = self.awareness_radius**2
        x1, y1 = self.position

        for soldier in soldiers:
            if soldier is self:
                continue

            x2, y2 = soldier.position

            dx = x2 - x1
            dy = y2 - y1

            distance_squared = dx * dx + dy * dy

            if distance_squared <= radius_squared:
                self.nearby_soldiers.append(soldier)

    def _get_direction(self) -> list[float]:
        if self.velocity is None:
            return self.direction

        x: float = self.velocity[0]
        y: float = self.velocity[1]

        magnitude: float = math.hypot(x, y)

        if magnitude == 0:
            return self.direction

        return [x / magnitude, y / magnitude]

    def _draw_direction_line(self, screen: Surface) -> None:
        if self.direction is None:
            return

        start_pos = self.position
        end_pos = [
            self.position[0] + self.direction[0] * self.size,
            self.position[1] + self.direction[1] * self.size,
        ]

        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)
