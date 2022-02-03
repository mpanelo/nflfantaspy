import os
import repo
import models

from nflrequests import LeagueHistoryRequests
from scraper import SeasonScraper

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
NUM_WEEKS_IN_SEASON = [16, 16, 16, 16, 16, 16, 16, 17]
SEASON_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def main():
    requests = LeagueHistoryRequests(NFL_FF_LEAGUE_ID, 2021)
    seasons = []
    for i, year in enumerate(SEASON_YEARS):
        if i < 5:
            # temporary until I can send all requests or sleep between scraping
            continue

        num_weeks = NUM_WEEKS_IN_SEASON[i]
        scraper = SeasonScraper(requests, year, num_weeks)
        print(f"scraping Season {year}")
        seasons.append(scraper.scrape())

    league = models.League(seasons, [])
    repo.commit(league, "league.json")


if __name__ == "__main__":
    main()
