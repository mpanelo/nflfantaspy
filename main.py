from dataclasses import asdict
import os
import re
import repo
import requests

from bs4 import BeautifulSoup
from models import Team, Teams

attr_team_id = re.compile("teamId-[0-9]")

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
NFL_FF_LEAGUE_URL = f"https://fantasy.nfl.com/league/{NFL_FF_LEAGUE_ID}"
NFL_FF_TEAM_URL = f"{NFL_FF_LEAGUE_URL}/team"

TEAM_ID_PREFIX = "teamId-"

TEAMS_JSON = "teams.json"
NFL_FF_GAMECENTER_URL = f"{NFL_FF_TEAM_URL}/" + "{team_id}/gamecenter?week={week}"


def fetch_teams():
    res = requests.get(NFL_FF_LEAGUE_URL)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "html.parser")
    span_tags = soup.find_all("span", attrs={"class": attr_team_id})

    team_ids = set(parse_team_id(span) for span in span_tags)
    teams = []

    for team_id in team_ids:
        res = requests.get(NFL_FF_TEAM_URL + f"/{team_id}")
        res.raise_for_status()

        soup = BeautifulSoup(res.content, "html.parser")

        span = soup.find(
            "span", attrs={"class": "selecter-item", "data-value": team_id}
        )
        if span is None:
            raise Exception(
                f"failed to find span tag containing the team name for team id: {team_id}"
            )
        name = span.get_text().strip().lower()

        anchor = soup.find("a", attrs={"class": "userName"})
        if anchor is None:
            raise Exception(
                f"failed to find anchor tag containing the team owner name for team id: {team_id}"
            )
        owner = anchor.get_text().strip().lower()
        teams.append(Team(team_id, name, owner))

    return Teams(teams)


def parse_team_id(span):
    for val in span.attrs["class"]:
        if val.startswith(TEAM_ID_PREFIX):
            return int(val.strip(TEAM_ID_PREFIX))


def main():
    if repo.exists(TEAMS_JSON):
        print(f"reading {TEAMS_JSON}")
        teams = repo.read(TEAMS_JSON, Teams)
    else:
        print(f"sending requests to NFL to fetch team data")
        teams = fetch_teams()
        repo.commit(teams, TEAMS_JSON)

    print(repo.read(TEAMS_JSON, Teams))


if __name__ == "__main__":
    main()
