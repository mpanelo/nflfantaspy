from typing import Type

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


class Teams(FantasyHistory):
    def __init__(self, league_id: int, fetch_fn, parser_class: Type[Parser]):
        super().__init__(league_id, fetch_fn, parser_class, "owners")


class Schedule(FantasyHistory):
    def __init__(self, league_id: int, fetch_fn, parser_class: Type[Parser]):
        super().__init__(league_id, fetch_fn, parser_class, "schedule")

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
            "leagueId": self.league_id,
            "scheduleDetail": page,
            "scheduleType": "week",
            "standingsTab": "schedule",
        }
