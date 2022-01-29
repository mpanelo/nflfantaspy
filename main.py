from dataclasses import dataclass
import contentparser
import ffclient
import os
import repo

from models import Team, Teams


NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
TEAMS_JSON = "teams.json"


@dataclass
class TeamStats:
    team_id: int
    team_name: str
    record: str
    streak: str
    waiver: int
    score: float


@dataclass
class Game:
    home: TeamStats
    away: TeamStats


json = [{"year": 2021, "schedule": [[{}]]}]


def fetch_scoring_data():
    from bs4 import BeautifulSoup

    client = ffclient.FantasyFootballClient(NFL_FF_LEAGUE_ID)
    content = client.get_league_history(year=2021, week=1)

    soup = BeautifulSoup(content, "html.parser")
    items = soup("li", attrs={"class": "matchup"})

    for item in items:
        team_wraps = item.find_all("div", attrs={"class": "teamWrap"})
        for team_wrap in team_wraps:
            anchor = team_wrap.find("a", attrs={"class": "teamName"})
            score = team_wrap.find("div", attrs={"class": "teamTotal"})
            print(anchor.text, score.text)


# def fetch_teams():
#     client = ffclient.FantasyFootballClient(NFL_FF_LEAGUE_ID)
#     team_ids = contentparser.parse_team_ids(client.get_league_content())

#     teams = []
#     for team_id in team_ids:
#         content = client.get_team_content(team_id)
#         (name, owner) = contentparser.parse_team_info(content, team_id)
#         teams.append(Team(team_id, name, owner))

#     return Teams(teams)


def main():
    fetch_scoring_data()


if __name__ == "__main__":
    main()
