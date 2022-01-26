from dataclasses import dataclass


@dataclass
class Team:
    id: int
    name: str = ""
    owner: str = ""


@dataclass
class Teams:
    teams: list[Team]
