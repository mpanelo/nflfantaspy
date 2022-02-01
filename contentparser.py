import re

from models import Game, Teams, Team
from bs4 import BeautifulSoup, Tag

ATTR_TEAM_ID = re.compile("teamId-[0-9]")
TEAM_ID_PREFIX = "teamId-"


def _parse_team_id(classes: list[str], team_id_prefix="teamId-") -> int:
    for cls in classes:
        if cls.startswith(team_id_prefix):
            return int(cls.strip(team_id_prefix))

    raise Exception(f"unable to find team ID in attribute")


class Paser(object):
    def __init__(self, content: bytes):
        self.soup = BeautifulSoup(content, "html.parser")


class TeamParser(Paser):
    def parse_teams(self):
        tbody = self.soup.find("tbody")
        trs = tbody.find_all("tr")

        teams = []
        for tr in trs:
            teams.append(self._parse_team(tr))

        return Teams(teams)

    def _parse_team(self, tr: Tag):
        id = _parse_team_id(tr.attrs["class"], "team-")

        td = tr.find("td", attrs={"class": "teamOwnerName"})
        span = td.find("span", attrs={"class": "userName"})
        owner = span.get_text().strip().lower()

        td = tr.find("td", attrs={"class": "teamImageAndName"})
        anchor = td.find("a", attrs={"class": "teamName"})
        team_name = anchor.get_text().strip().lower()

        return Team(id, team_name, owner)


class ScheduleContentParser:
    def __init__(self, content: bytes):
        self.soup = BeautifulSoup(content, "html.parser")

    def parse_games(self, week: int):
        games = []
        for matchup in self._find_matchups():
            games.append(self._parse_game(matchup, week))
        return games

    def _find_matchups(self):
        return self.soup.find_all("li", attrs={"class": "matchup"})

    def _parse_game(self, matchup, week):
        home, away = matchup.find_all("div", attrs={"class": "teamWrap"})
        home_id, home_score = self._find_team_id(home), self._find_team_total(home)
        away_id, away_score = self._find_team_id(away), self._find_team_total(away)
        return Game(week, home_id, away_id, home_score, away_score)

    def _find_team_id(self, team):
        result = team.find("a", attrs={"class": ATTR_TEAM_ID})

        for cl in result.attrs["class"]:
            if cl.startswith(TEAM_ID_PREFIX):
                return int(cl.strip(TEAM_ID_PREFIX))

        raise Exception(f"no {TEAM_ID_PREFIX}[0-9]+ class found in {result}")

    def _find_team_total(self, team):
        result = team.find("div", attrs={"class": "teamTotal"})
        return float(result.text)
