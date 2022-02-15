from typing import Type

from nflfantaspy import constants
from nflfantaspy.parser import Parser


class FantasyHistory:
    def __init__(
        self, league_id: int, fetch_fn, parser_class: Type[Parser], content_type: str
    ):
        self.league_id = league_id
        self.base_url = f"https://fantasy.nfl.com/league/{league_id}/history"
        self.fetch_fn = fetch_fn
        self.parser_class = parser_class
        self.content_type = content_type

    def execute(self, **kwargs):
        year = kwargs["year"]
        url = f"{self.base_url}/{year}/{self.content_type}"
        content = self.fetch_fn(url, params=self._get_params(**kwargs))
        parser = self.parser_class(content)
        return parser.parse()

    def _get_params(self, **kwargs):
        return None


class Playoffs(FantasyHistory):
    def __init__(self, league_id: int, fetch_fn, parser_class: Type[Parser]):
        super().__init__(league_id, fetch_fn, parser_class, "playoffs")

    def _get_params(self, **kwargs):
        return {
            "bracketType": kwargs["bracket_type"],
            "standingsTab": "playoffs",
        }


class Teams(FantasyHistory):
    def __init__(self, league_id: int, fetch_fn, parser_class: Type[Parser]):
        super().__init__(league_id, fetch_fn, parser_class, "owners")


class Schedule(FantasyHistory):
    def __init__(self, league_id: int, fetch_fn, parser_class: Type[Parser]):
        super().__init__(league_id, fetch_fn, parser_class, "schedule")

    def execute(self, year: int, **kwargs):
        page = 1
        data = []
        while True:
            games = super().execute(year=year, page=page)
            if games == []:
                print(f"no games found for week {page}")
                break
            data.extend(games)
            page += 1
        return data

    def _get_params(self, year: int, page: int):
        return {
            "gameSeason": year,
            "leagueId": self.league_id,
            "scheduleDetail": page,
            "scheduleType": "week",
            "standingsTab": "schedule",
        }


class Games(FantasyHistory):
    def __init__(self, schedule: Schedule, playoffs: Playoffs):
        self.schedule = schedule
        self.playoffs = playoffs

    def execute(self, **kwargs):
        games = self.schedule.execute(**kwargs)
        playoffs = self.playoffs.execute(**kwargs)

        for game in games:
            if game["week"] not in playoffs["weeks"]:
                game["type"] = constants.GAME_TYPE_REGULAR
            elif game["home_id"] in playoffs["teams"]:
                game["type"] = constants.GAME_TYPE_PLAYOFF
            else:
                game["type"] = constants.GAME_TYPE_CONSOLATION
        return games
