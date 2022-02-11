from typing import Type

from nflfantaspy.settings import NFL_FF_LEAGUE_ID
from nflfantaspy.parser.base import BaseParser


class FantasyHistory:
    BASE_URL = f"https://fantasy.nfl.com/league/{NFL_FF_LEAGUE_ID}/history"

    def __init__(self, fetch_fn, parser_class: Type[BaseParser], content_type: str):
        self.fetch_fn = fetch_fn
        self.parser_class = parser_class
        self.content_type = content_type

    def execute(self, **kwargs):
        year = kwargs["year"]
        url = f"{self.BASE_URL}/{year}/{self.content_type}"
        content = self.fetch_fn(url, params=self._get_params(**kwargs))
        parser = self.parser_class(content)
        return parser.parse()

    def _get_params(self, **kwargs):
        return None


class Teams(FantasyHistory):
    def __init__(self, fetch_fn, parser_class):
        super().__init__(fetch_fn, parser_class, "owners")


class Schedule(FantasyHistory):
    def __init__(self, fetch_fn, parser_class):
        super().__init__(fetch_fn, parser_class, "schedule")

    def execute(self, year: int):
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
            "leagueId": NFL_FF_LEAGUE_ID,
            "scheduleDetail": page,
            "scheduleType": "week",
            "standingsTab": "schedule",
        }
