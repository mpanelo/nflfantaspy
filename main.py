from dataclasses import dataclass, asdict
import os
from bs4 import BeautifulSoup
import requests
import re
import json

attr_team_id = re.compile("teamId-[0-9]")

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
NFL_FF_LEAGUE_URL = f"https://fantasy.nfl.com/league/{NFL_FF_LEAGUE_ID}"
NFL_FF_TEAM_URL = f"{NFL_FF_LEAGUE_URL}/team"

TEAM_ID_PREFIX = "teamId-"

@dataclass
class Team:
    """Class for teams in an NFL FF league"""
    id: int
    name: str = ""
    owner: str = ""

def parse_team_id(span):
    for val in span.attrs["class"]:
        if val.startswith(TEAM_ID_PREFIX):
            return val.strip(TEAM_ID_PREFIX)


def initialize_teams(team_ids):
    teams = {team_id: Team(team_id) for team_id in team_ids}

    for team_id in teams:
        res = requests.get(NFL_FF_TEAM_URL + f"/{team_id}")
        res.raise_for_status()

        soup = BeautifulSoup(res.content, "html.parser")

        span = soup.find("span", attrs={"class": "selecter-item", "data-value": team_id})
        if span is None:
            raise Exception(f"failed to find span tag containing the team name for team id: {team_id}")
        teams[team_id].name = span.get_text().strip().lower()

        anchor = soup.find("a", attrs={"class": "userName"})
        if anchor is None:
            raise Exception(f"failed to find anchor tag containing the team owner name for team id: {team_id}")
        teams[team_id].owner = anchor.get_text().strip().lower()

    return teams

def save_as_json(teams):
    payload = {"teams": []}
    
    for _, team in teams.items():
        payload["teams"].append(asdict(team))

    with open("payload.json", "w") as f:
        json.dump(payload, f, indent=4, sort_keys=True)

def main():
    res = requests.get(NFL_FF_LEAGUE_URL)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "html.parser")
    span_tags = soup.find_all("span", attrs={"class": attr_team_id})

    team_ids = set(parse_team_id(span) for span in span_tags)
    teams = initialize_teams(team_ids)
    save_as_json(teams)


if __name__ == "__main__":
    main()