import re

from models import Game
from bs4 import BeautifulSoup

ATTR_TEAM_ID = re.compile("teamId-[0-9]")
TEAM_ID_PREFIX = "teamId-"

TEAM_ID = "TEAM_ID"
TEAM_NAME = "TEAM_NAME"
TEAM_OWNER = "TEAM_OWNER"

TAG = "name"
ATTRS = "attrs"

SOUP_KWARGS_BY_FIELD = {
    TEAM_ID: {TAG: "span", ATTRS: {"class": ATTR_TEAM_ID}},
    TEAM_NAME: {
        TAG: "span",
        ATTRS: {"class": "selecter-item"},
    },
    TEAM_OWNER: {TAG: "a", ATTRS: {"class": "userName"}},
}


def parse_team_ids(content: bytes):
    soup = BeautifulSoup(content, "html.parser")
    team_id_kwargs = SOUP_KWARGS_BY_FIELD[TEAM_ID]
    span_tags = soup.find_all(**team_id_kwargs)

    classes = []
    for span in span_tags:
        classes.extend(
            cl for cl in span.attrs["class"] if cl.startswith(TEAM_ID_PREFIX)
        )

    return set(int(cl.strip(TEAM_ID_PREFIX)) for cl in classes)


def parse_team_info(content: bytes, team_id: int):
    soup = BeautifulSoup(content, "html.parser")

    team_name_kwargs = SOUP_KWARGS_BY_FIELD[TEAM_NAME]
    team_owner_kwargs = SOUP_KWARGS_BY_FIELD[TEAM_OWNER]

    name = _parse_tag_text(soup, team_name_kwargs, {"data-value": team_id})
    owner = _parse_tag_text(soup, team_owner_kwargs)

    return (name, owner)


def _parse_tag_text(soup: BeautifulSoup, kwargs: dict, custom_attrs={}):
    kwargs[ATTRS] = kwargs[ATTRS] | custom_attrs
    tag = soup.find(**kwargs)

    if tag is None:
        raise Exception(f"unable to find tag {kwargs[TAG]}")

    return tag.get_text().strip().lower()


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
