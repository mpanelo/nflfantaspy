import requests


class LeagueHistoryRequests(object):
    def __init__(self, league_id: int, year: int):
        self.league_id = league_id
        self.year = year
        self.base_url = f"https://fantasy.nfl.com/league/{league_id}/history/{year}"

    def fetch_teams(self) -> bytes:
        url = f"{self.base_url}/owners"
        return self._get_content(url)

    def fetch_schedule(self, week: int) -> bytes:
        url = f"{self.base_url}/schedule"
        payload = {
            "gameSeason": self.year,
            "leagueId": self.league_id,
            "scheduleDetail": week,
            "scheduleType": "week",
            "standingsTab": "schedule",
        }
        return self._get_content(url, payload)

    def _get_content(self, url: str, payload={}) -> bytes:
        print(f"sending request to {url}")
        res = requests.get(url, params=payload)
        res.raise_for_status()
        return res.content
