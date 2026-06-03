from enum import Enum


class Team(Enum):
    RED = 1
    GREEN = 2


TEAM_COLORS = {Team.RED: (200, 25, 50), Team.GREEN: (50, 200, 25)}
