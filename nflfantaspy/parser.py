import abc
import re

from bs4 import BeautifulSoup, Tag

REGEX_TEAM_ID = re.compile("teamId-[0-9]")
REGEX_PLAYOFF_WEEK = re.compile("\d+")


class Parser(abc.ABC):
    def __init__(self, content: bytes):
        self.soup = BeautifulSoup(content, "html.parser")

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError


class Schedule(Parser):
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
        anchor = team.find("a", attrs={"class": REGEX_TEAM_ID})
        return _parse_team_id(anchor)

    def _parse_team_score(self, team):
        result = team.find("div", attrs={"class": "teamTotal"})
        return float(result.text)


class Teams(Parser):
    def parse(self) -> list[dict]:
        tbody = self.soup.find("tbody")
        trs = tbody.find_all("tr")

        teams = []
        for tr in trs:
            teams.append(self._parse_team(tr))
        return teams

    def _parse_team(self, tr: Tag):
        id = _parse_team_id(tr, team_id_prefix="team-")

        td = tr.find("td", attrs={"class": "teamOwnerName"})
        span = td.find("span", attrs={"class": "userName"})
        owner = span.get_text().strip().lower()

        td = tr.find("td", attrs={"class": "teamImageAndName"})
        anchor = td.find("a", attrs={"class": "teamName"})
        name = anchor.get_text().strip().lower()

        return {"id": id, "name": name, "owner": owner}


class Settings(Parser):
    def parse(self):
        playoff_weeks = self._parse_playoff_weeks()
        return {"weeks": playoff_weeks[-1], "playoff_weeks": playoff_weeks}

    def _parse_playoff_weeks(self):
        tag = self.soup.find("em", string="Playoffs")
        div = tag.next_sibling
        text = div.string

        playoff_weeks, _ = text.strip().split("-")
        matches = REGEX_PLAYOFF_WEEK.findall(playoff_weeks)

        return [int(match) for match in matches]


def _parse_team_id(tag: Tag, team_id_prefix="teamId-") -> int:
    for cls in tag.attrs["class"]:
        if cls.startswith(team_id_prefix):
            return int(cls.strip(team_id_prefix))

    raise Exception(f"no {team_id_prefix}[0-9]+ class found in {tag}")
