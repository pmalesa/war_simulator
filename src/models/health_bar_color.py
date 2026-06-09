from enum import Enum


class HealthBarColor(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3


HEALTH_BAR_COLORS = {
    HealthBarColor.RED: (255, 40, 0),
    HealthBarColor.YELLOW: (252, 202, 3),
    HealthBarColor.GREEN: (3, 252, 11),
}
