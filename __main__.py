from collections import defaultdict

from nflfantaspy.fetcher import http
from nflfantaspy import settings
from nflfantaspy.parser import teams, schedule
from nflfantaspy import spyder
from nflfantaspy.db.backends import airtable


def main():
    spy = spyder.Schedule(http.get, schedule.Parser)
    data = crawl(spy, settings.NFL_FF_LEAGUE_ACTIVE_YEARS[:3])
    cfg = {
        "api_key": settings.AIRTABLE_API_KEY,
        "base_id": settings.AIRTABLE_BASE_GAMES_ID,
    }
    db = airtable.DatabaseClient(cfg)
    for year, records in data.items():
        db.table = str(year)
        db.save(records)


def crawl(spy: spyder.FantasyHistory, active_years: list[int]):
    data = defaultdict(list)
    for year in active_years:
        data[year] = spy.execute(year=year)
    return data


if __name__ == "__main__":
    main()
