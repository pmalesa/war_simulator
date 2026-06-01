import math
import random

import pygame
from pygame import Surface


class Soldier:
    MAX_HEALTH: int = 100
    DEFAULT_STEP: int = 1
    DEFAULT_SIZE: int = 10
    DEFAULT_AWARENESS_RADIUS = 10
    DEFAULT_FIELD_OF_VIEW_RADIUS = 100
    DEFAULT_FIELD_OF_VIEW_ANGLE = 60
    DEFAULT_FIELD_OF_VIEW_RANGE = 100
    TURN_ANGLE = 15

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
        fov_angle: int = DEFAULT_FIELD_OF_VIEW_ANGLE,
        fov_range: int = DEFAULT_FIELD_OF_VIEW_RANGE,
        nearby_soldiers: list["Soldier"] | None = None,
    ):
        self.id = id
        self.name = name
        self.health = health

        self.velocity = velocity if velocity is not None else [1, 1]
        self.position = position if position is not None else [0, 0]
        self.angle: float = 0.0
        self.facing_angle: float = 0.0

        self.default_color = color if color is not None else (255, 0, 0)
        self.color = color if color is not None else (255, 0, 0)
        self.direction_line_color = (0, 0, 0)
        self.team = team

        self.size = size
        self.step = step

        self.awareness_radius = awareness_radius
        self.fov_angle = fov_angle
        self.fov_range = fov_range

        self.nearby_soldiers = nearby_soldiers if nearby_soldiers is not None else []
        self.visible_soldiers = []

    def shoot(self) -> None:
        pass

    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        return self.health > 0

    def move(self, screen: Surface) -> None:
        if not self.velocity:
            return

        self._update_velocity_from_angle()

        self.position[0] += self.velocity[0] * self.step
        self.position[1] += self.velocity[1] * self.step

        self.position[0] = max(0, min(self.position[0], screen.get_width() - self.size))
        self.position[1] = max(0, min(self.position[1], screen.get_height() - self.size))

        self._update_angle()

        if self._is_edge_ahead(screen):
            self._turn_right()

        if self._is_someone_ahead():
            self.color = (255, 255, 0)
            self.direction_line_color = (255, 0, 0)
        else:
            self.color = self.default_color
            self.direction_line_color = (0, 0, 0)

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

        if self.visible_soldiers:
            x1, y2 = self.position
            x2, y2 = self.visible_soldiers[0].position

            target_x = x2 - x1
            target_y = y2 - y2
            cross = self.velocity[0] * target_y - self.velocity[1] * target_x

            if cross > 0:
                self._turn_left()
            else:
                self._turn_right()

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

    def update_visible_soldiers(self, soldiers: list["Soldier"]) -> None:
        self.visible_soldiers = []

        if self.angle is None:
            return

        direction_x, direction_y = self._get_direction()

        radius_squared = self.fov_range**2
        x1, y1 = self.position

        half_fov = self.fov_angle / 2
        cos_limit = math.cos(math.radians(half_fov))

        for soldier in soldiers:
            if soldier is self:
                continue

            x2, y2 = soldier.position

            dx = x2 - x1
            dy = y2 - y1

            distance_squared = dx * dx + dy * dy

            if distance_squared > radius_squared:
                continue

            distance = max(0.0001, math.sqrt(distance_squared))

            target_x = dx / distance
            target_y = dy / distance

            dot = direction_x * target_x + direction_y * target_y

            if dot >= cos_limit:
                self.visible_soldiers.append(soldier)

    def _draw_direction_line(self, screen: Surface) -> None:
        if self.angle is None:
            return

        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)

        start_pos = self.position
        end_pos = [
            self.position[0] + dx * self.size,
            self.position[1] + dy * self.size,
        ]

        pygame.draw.line(screen, self.direction_line_color, start_pos, end_pos, 2)

    def _is_someone_ahead(self) -> bool:
        for soldier in self.visible_soldiers:
            if self.team != soldier.team:
                return True
        return False

    def _get_direction(self) -> tuple[float, float]:
        angle_rad = math.radians(self.angle)
        return (math.cos(angle_rad), math.sin(angle_rad))

    def _update_angle(self) -> None:
        if self.velocity is None:
            return

        vx, vy = self.velocity

        if vx == 0 and vy == 0:
            return

        self.angle = math.degrees(math.atan2(vy, vx))

    def _turn_left(self) -> None:
        self.angle = (self.angle - self.TURN_ANGLE) % 360

    def _turn_right(self) -> None:
        self.angle = (self.angle + self.TURN_ANGLE) % 360

    def _update_velocity_from_angle(self) -> None:
        angle_rad: float = math.radians(self.angle)
        self.velocity = [math.cos(angle_rad), math.sin(angle_rad)]

    def _is_edge_ahead(self, screen: Surface) -> bool:
        dx, dy = self._get_direction()

        lookahead = self.size * 4

        future_x = self.position[0] + dx * lookahead
        future_y = self.position[1] + dy * lookahead

        return (
            future_x <= self.size
            or future_x >= screen.get_width() - self.size
            or future_y <= self.size
            or future_y >= screen.get_height() - self.size
        )
