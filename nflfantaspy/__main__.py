import argparse
from collections import defaultdict

from nflfantaspy.fetcher import http
from nflfantaspy import settings
from nflfantaspy import parser
from nflfantaspy import spyder
from nflfantaspy.db.backends import airtable, json

# for year in years: (spyder: schedule, playoffs).execute() => post-processing => db.save


def main():
    args = parse_args()
    spy = spyder.Schedule(args.league, http.get, parser.Schedule)
    data = crawl(spy, settings.NFL_FF_LEAGUE_ACTIVE_YEARS[:1])

    if args.backend == settings.BACKENDS_JSON:
        save_to_json(data)
    elif args.backend == settings.BACKENDS_AIRTABLE:
        save_to_airtable(data)
    else:
        raise Exception(f"backend {args.backend} is not supported")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape game and team history from your NFL fantasy football league. Store it as JSON or on Airtable."
    )
    parser.add_argument("--league", type=int, required=True)
    parser.add_argument("--backend", choices=settings.BACKENDS, required=True)
    return parser.parse_args()


def save_to_json(data: list[dict]):
    db = json.DatabaseClient({"filename": "games.json"})
    db.save(data)


def save_to_airtable(data: list[dict]):
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
