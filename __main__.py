import os

# import models

from nflfantaspy.nfl.client import NFLClient
from nflfantaspy.parser import teams
from nflfantaspy.db.backends.json import client

# from nflrequests import LeagueHistoryRequests
# from scraper import SeasonScraper

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
# NUM_WEEKS_IN_SEASON = [16, 16, 16, 16, 16, 16, 16, 17]
# SEASON_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def main():
    nfl = NFLClient(NFL_FF_LEAGUE_ID)
    res = nfl.get_teams(year=2021)
    parser = teams.Parser(res.content)
    games = parser.parse()
    db = client.DatabaseClient("teams.json")
    db.save(games)


if __name__ == "__main__":
    main()
