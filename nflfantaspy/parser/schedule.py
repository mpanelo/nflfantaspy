import re

from nflfantaspy.parser.base import BaseParser
from nflfantaspy.parser import utils

ATTR_TEAM_ID = re.compile("teamId-[0-9]")


class Parser(BaseParser):
    def parse(self) -> list[dict]:
        games = []
        week = self._parse_week()
        for matchup in self._find_matchups():
            game = self._parse_game(matchup)
            game["week"] = week
            games.append(game)
        return games

    def _parse_week(self):
        ul = self.soup.find("ul", attrs={"class": "scheduleWeekNav"})
        li = ul.find("li", class_="selected")
        span = li.find("span", class_="title")

        return int(span.string)

    def _find_matchups(self):
        return self.soup.find_all("li", attrs={"class": "matchup"})

    def _parse_game(self, matchup):
        home, away = matchup.find_all("div", attrs={"class": "teamWrap"})
        home_id, home_score = self._parse_team_id(home), self._parse_team_score(home)
        away_id, away_score = self._parse_team_id(away), self._parse_team_score(away)

        return {
            "home_id": home_id,
            "home_score": home_score,
            "away_id": away_id,
            "away_score": away_score,
        }

    def _parse_team_id(self, team):
        anchor = team.find("a", attrs={"class": ATTR_TEAM_ID})
        return utils.parse_team_id(anchor)

    def _parse_team_score(self, team):
        result = team.find("div", attrs={"class": "teamTotal"})
        return float(result.text)
