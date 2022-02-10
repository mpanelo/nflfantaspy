import requests


class Client:
    def __init__(self, league_id: int):
        self.league_id = league_id
        self.base_url = f"https://fantasy.nfl.com/league/{league_id}"

    def get_teams(self, year: int):
        url = f"{self.base_url}/history/{year}/owners"
        response = requests.get(url)
        response.raise_for_status()
        return response

    def get_schedule(self, year: int, week: int) -> bytes:
        url = f"{self.base_url}/history/{year}/schedule"
        payload = {
            "gameSeason": year,
            "leagueId": self.league_id,
            "scheduleDetail": week,
            "scheduleType": "week",
            "standingsTab": "schedule",
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response

    def get_settings(self, year):
        url = f"{self.base_url}/history/{year}/settings"
        response = requests.get(url)
        response.raise_for_status()
        return response
