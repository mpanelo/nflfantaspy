from dataclasses import dataclass, field


@dataclass
class Team:
    id: int
    name: str = ""
    owner: str = ""


@dataclass
class Teams:
    teams: list[Team]


@dataclass
class Game:
    week: int
    home_id: int
    away_id: int
    home_score: float
    away_score: float


@dataclass
class Season:
    year: int
    games: list[Game]
    standings: list[int] = field(default_factory=list)


@dataclass
class Seasons:
    seasons: list[Season]


@dataclass
class League:
    seasons: Seasons
    teams: Teams
