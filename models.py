from dataclasses import dataclass


GAME_TYPE_REGULAR = "REGULAR"
GAME_TYPE_PLAYOFF = "PLAYOFF"
GAME_TYPE_CONSOLATION = "CONSOLATION"


@dataclass
class Team:
    nfl_id: int
    name: str = ""
    owner: str = ""


@dataclass
class Game:
    week: int
    home_id: int
    away_id: int
    home_score: float
    away_score: float
    type: str


@dataclass
class Season:
    year: int
    games: list[Game]
    teams: list[Team]


@dataclass
class League:
    seasons: list[Season]
