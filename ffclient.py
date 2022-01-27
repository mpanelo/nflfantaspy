import requests


class FantasyFootballClient:
    def __init__(self, league_id: int):
        self.league_id = league_id
        self.base_url = f"https://fantasy.nfl.com/league/{league_id}"

    def get_league_content(self) -> bytes:
        return self._get_content(self.base_url)

    def get_team_content(self, team_id: int) -> bytes:
        url = self.base_url + f"/team/{team_id}"
        return self._get_content(url)

    def get_schedule_content(self, year: int) -> bytes:
        url = self.base_url + f"/history/{year}/schedule"
        return self._get_content(url)

    def _get_content(self, url: str) -> bytes:
        res = requests.get(url)
        res.raise_for_status()
        return res.content
