import contentparser
import ffclient
import os
import repo

from models import Team, Teams


NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
TEAMS_JSON = "teams.json"


def fetch_teams():
    client = ffclient.FantasyFootballClient(NFL_FF_LEAGUE_ID)
    team_ids = contentparser.parse_team_ids(client.get_league_content())

    teams = []
    for team_id in team_ids:
        content = client.get_team_content(team_id)
        (name, owner) = contentparser.parse_team_info(content, team_id)
        teams.append(Team(team_id, name, owner))

    return Teams(teams)


def main():
    if repo.exists(TEAMS_JSON):
        print(f"reading {TEAMS_JSON}")
        teams = repo.read(TEAMS_JSON, Teams)
    else:
        print(f"sending requests to NFL to fetch team data")
        teams = fetch_teams()
        repo.commit(teams, TEAMS_JSON)


if __name__ == "__main__":
    main()
