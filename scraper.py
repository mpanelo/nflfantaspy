from models import Season, Team
from contentparser import TeamParser, ScheduleParser
from nflrequests import LeagueHistoryRequests


class Scraper(object):
    def __init__(self, requests: LeagueHistoryRequests):
        self.requests = requests


class SeasonScraper(Scraper):
    def __init__(self, requests: LeagueHistoryRequests, year: int, num_weeks=17):
        super().__init__(requests)
        self.year = year
        self.num_weeks = num_weeks

    def scrape(self) -> Season:
        games = []
        for week in range(1, self.num_weeks + 1):
            print(f"fetching week {week} content")
            content = self.requests.fetch_schedule(week)
            parser = ScheduleParser(content, week)
            games.extend(parser.parse_schedule())
        return Season(self.year, games)


class TeamScraper(Scraper):
    def scrape(self) -> list[Team]:
        content = self.requests.fetch_teams()
        parser = TeamParser(content)
        return parser.parse_teams()
