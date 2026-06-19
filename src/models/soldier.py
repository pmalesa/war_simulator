import math
import random
from enum import IntEnum

import pygame
from pygame import Rect, Surface

from src.models.health_bar_color import HEALTH_BAR_COLORS, HealthBarColor
from src.models.projectile import Projectile
from src.models.wall import Wall


class SoldierAction(IntEnum):
    MOVE_FORWARD = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2
    SHOOT = 3
    DO_NOTHING = 4

    @classmethod
    def count(cls) -> int:
        return len(cls)


class Soldier:
    MAX_HEALTH: int = 100
    DEFAULT_STEP: int = 2
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
        max_health: int = MAX_HEALTH,
        position: list[float] | None = None,
        team: int = 1,
        color: tuple[int] | None = None,
        size: int = DEFAULT_SIZE,
        step_size: int = DEFAULT_STEP,
        awareness_radius: int = DEFAULT_AWARENESS_RADIUS,
        fov_angle: int = DEFAULT_FIELD_OF_VIEW_ANGLE,
        fov_range: int = DEFAULT_FIELD_OF_VIEW_RANGE,
        nearby_soldiers: list["Soldier"] | None = None,
    ):
        self.id = id
        self.name = name
        self.current_health = max_health
        self.max_health = max_health

        self.velocity: list[float] = [0, 0]
        self.position = position if position is not None else [0, 0]
        self.angle: float = float(random.randint(0, 360))
        self.facing_angle: float = 0.0
        self.active: bool = True

        self.default_color = color if color is not None else (255, 0, 0)
        self.color = color if color is not None else (255, 0, 0)
        self.direction_line_color = (0, 0, 0)
        self.team = team

        self.size = size
        self.step_size = step_size

        self.awareness_radius = awareness_radius
        self.fov_angle = fov_angle
        self.fov_range = fov_range

        self.nearby_soldiers = nearby_soldiers if nearby_soldiers is not None else []
        self.visible_soldiers = []

    def step(self, action_id: int, screen: Surface) -> None:
        if not self.active:
            return

        action = SoldierAction(action_id)
        match action:
            case SoldierAction.MOVE_FORWARD:
                self._move(screen)
            case SoldierAction.TURN_LEFT:
                self._turn_left()
            case SoldierAction.TURN_RIGHT:
                self._turn_right()
            case SoldierAction.SHOOT:
                self._shoot()
            case SoldierAction.DO_NOTHING:
                pass

    def take_damage(self, damage: int) -> None:
        self.current_health = max(0, self.current_health - damage)
        if self.current_health == 0:
            self.active = False

    def is_alive(self) -> bool:
        return self.current_health > 0

    def update(self, screen: Surface, walls: list[Wall], soldiers: list["Soldier"]) -> None:
        if not self.active:
            return

        self._update_nearby_soldiers(soldiers)
        self._update_visible_soldiers(soldiers)

        if self._collides_with_wall(walls):
            self._resolve_wall_collision(walls)
            return

        if self._collides_with_soldier(soldiers):
            self._resolve_soldier_collision(soldiers)
            return

        if self._is_wall_ahead(walls):
            if random.choice([True, False]):
                self._turn_left(90)
            else:
                self._turn_right(90)

        if self._is_edge_ahead(screen):
            if random.choice([True, False]):
                self._turn_right(90)
            else:
                self._turn_left(90)

        if self._is_someone_ahead():
            self.color = (255, 255, 0)
            self.direction_line_color = (255, 0, 0)
        else:
            self.color = self.default_color
            self.direction_line_color = (0, 0, 0)

    def draw(self, screen: Surface) -> None:
        if not self.active:
            return

        if not isinstance(screen, Surface) or not screen:
            raise RuntimeError(
                f"Invalid type of screen object: {type(screen)} instead of pygame.Surface."
            )
        pygame.draw.circle(screen, self.color, self.position, self.size)
        self._draw_direction_line(screen)
        self._draw_health_bar(screen)

    def _update_nearby_soldiers(self, soldiers: list["Soldier"]) -> None:
        if not self.active:
            return

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

    def _update_visible_soldiers(self, soldiers: list["Soldier"]) -> None:
        if not self.active:
            return

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

    def respawn(self, screen: Surface) -> None:
        self.active = True
        self.current_health = self.max_health
        self.position = [
            random.randint(self.size, screen.get_width() - self.size),
            random.randint(self.size, screen.get_height() - self.size),
        ]

    # TODO: To remove
    def get_rect(self) -> Rect:
        return Rect(
            self.position[0] - self.size, self.position[1] - self.size, self.size * 2, self.size * 2
        )

    def _shoot(self) -> Projectile:
        return Projectile(
            position=self.position.copy(),
            angle=self.angle,
            team=self.team,
        )

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

    def _draw_health_bar(self, screen: Surface) -> None:
        health_percentage: float = self.current_health / self.max_health
        health_bar_fill: float = 2 * self.size * health_percentage
        start_pos = [self.position[0] - self.size, self.position[1] - 1.7 * self.size]
        end_pos = [start_pos[0] + health_bar_fill, start_pos[1]]

        if health_percentage >= 0.7:
            health_bar_color = HEALTH_BAR_COLORS[HealthBarColor.GREEN]
        elif health_percentage >= 0.3:
            health_bar_color = HEALTH_BAR_COLORS[HealthBarColor.YELLOW]
        else:
            health_bar_color = HEALTH_BAR_COLORS[HealthBarColor.RED]

        pygame.draw.line(screen, health_bar_color, start_pos, end_pos, 3)

    def _is_someone_ahead(self) -> bool:
        for soldier in self.visible_soldiers:
            if self.team != soldier.team:
                return True
        return False

    def _get_direction(self) -> tuple[float, float]:
        angle_rad: float = math.radians(self.angle)
        return (math.cos(angle_rad), math.sin(angle_rad))

    def _update_velocity(self) -> None:
        angle_rad: float = math.radians(self.angle)
        self.velocity = [math.cos(angle_rad) * self.step_size, math.sin(angle_rad) * self.step_size]

    def _move(self, screen: Surface) -> None:
        self._update_velocity()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[0] = max(self.size, min(self.position[0], screen.get_width() - self.size))
        self.position[1] = max(self.size, min(self.position[1], screen.get_height() - self.size))

    def _turn_left(self, angle: float = TURN_ANGLE) -> None:
        self.angle = (self.angle - angle) % 360

    def _turn_right(self, angle: float = TURN_ANGLE) -> None:
        self.angle = (self.angle + angle) % 360

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

    def _is_wall_ahead(self, walls: list[Wall]) -> bool:
        dx, dy = self._get_direction()
        lookahead = self.size * 4

        future_x = self.position[0] + dx * lookahead
        future_y = self.position[1] + dy * lookahead

        for wall in walls:
            if wall.rect.collidepoint(future_x, future_y):
                return True

        return False

    def _collides_with_wall(self, walls: list[Wall]) -> bool:
        soldier_rect = self.get_rect()

        for wall in walls:
            if soldier_rect.colliderect(wall.rect):
                return True

        return False

    def _collides_with_soldier(self, soldiers: list["Soldier"]) -> bool:
        for soldier in soldiers:
            if soldier == self:
                continue

            if not soldier.active:
                continue

            dx = self.position[0] - soldier.position[0]
            dy = self.position[1] - soldier.position[1]

            distance_squared = dx * dx + dy * dy

            collision_distance = self.size + soldier.size

            if distance_squared <= collision_distance**2:
                return True

        return False

    def _resolve_wall_collision(self, walls: list[Wall]) -> None:
        soldier_rect: Rect = self.get_rect()

        for wall in walls:
            if not soldier_rect.colliderect(wall.rect):
                continue

            overlap_left = soldier_rect.right - wall.rect.left
            overlap_right = wall.rect.right - soldier_rect.left
            overlap_top = soldier_rect.bottom - wall.rect.top
            overlap_bottom = wall.rect.bottom - soldier_rect.top

            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left:
                self.position[0] -= overlap_left
                self.angle = 180
            elif min_overlap == overlap_right:
                self.position[0] += overlap_right
                self.angle = 0
            elif min_overlap == overlap_top:
                self.position[1] -= overlap_top
                self.angle = 270
            else:
                self.position[1] += overlap_bottom
                self.angle = 90

            self.angle = (self.angle + random.uniform(-30, 30)) % 360

    def _resolve_soldier_collision(self, soldiers: list["Soldier"]) -> None:
        for soldier in soldiers:
            if soldier == self:
                continue

            if not soldier.active:
                continue

            dx = self.position[0] - soldier.position[0]
            dy = self.position[1] - soldier.position[1]

            distance = math.hypot(dx, dy)
            min_distance = self.size + soldier.size

            if distance >= min_distance:
                continue

            if distance == 0:
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
                distance = math.hypot(dx, dy)

            overlap = min_distance - distance

            push_x = dx / distance * overlap
            push_y = dy / distance * overlap

            self.position[0] += push_x / 2
            self.position[1] += push_y / 2

            soldier.position[0] -= push_x / 2
            soldier.position[1] -= push_y / 2

            self.angle = (math.degrees(math.atan2(push_y, push_x)) + random.uniform(-30, 30)) % 360

            if self.team != soldier.team:
                self.take_damage(10)
                soldier.take_damage(10)
