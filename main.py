import ffclient
import os
import repo


from models import Season
from contentparser import ScheduleContentParser

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
TEAMS_JSON = "teams.json"


def main():
    client = ffclient.FantasyFootballClient(NFL_FF_LEAGUE_ID)
    seasons = []
    for year in [2021]:
        games = []
        for week in range(1, 18):
            content = client.get_league_history(year, week)

            parser = ScheduleContentParser(content)
            games.extend(parser.parse_games(week))
        seasons.append(Season(year, games))

    repo.commit(seasons[0], "season-2021.json")


if __name__ == "__main__":
    main()
