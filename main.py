import os

from models import Season, Seasons, League, Teams
from contentparser import TeamParser, ScheduleContentParser
from nflrequests import LeagueHistoryRequests

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
WEEKS_IN_SEASON = [16, 16, 16, 16, 16, 16, 16, 17]
SEASON_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


class LeagueScraper(object):
    def __init__(self, requests: LeagueHistoryRequests):
        self.requests = requests

    def scrape():
        return League(Seasons([]), Teams([]))

    def _scrape_teams(self):
        content = self.requests.fetch_teams()
        parser = TeamParser(content)
        return parser.parse_teams()

    def _scrape_schedule(self, week: int):
        content = self.requests.fetch_schedule(week)
        parser = ScheduleContentParser(content)
        return parser.parse_games()


def main():
    requests = LeagueHistoryRequests(NFL_FF_LEAGUE_ID, 2021)
    scraper = LeagueScraper(requests)
    print(scraper._scrape_teams())


if __name__ == "__main__":
    main()
