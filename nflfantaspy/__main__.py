import argparse
from collections import defaultdict

from nflfantaspy.fetcher import http
from nflfantaspy import settings
from nflfantaspy import parser
from nflfantaspy import spyder
from nflfantaspy.db.backends import airtable, json
from nflfantaspy import cli

# for year in years: (spyder: schedule, playoffs).execute() => post-processing => db.save


def main():
    args = cli.parse_args()

    if args.data_type == cli.DATA_TYPE_GAMES:
        spy = spyder.Schedule(args.league_id, http.get, parser.Schedule)
    elif args.data_type == cli.DATA_TYPE_TEAMS:
        spy = spyder.Teams(args.league_id, http.get, parser.Teams)
    else:
        raise Exception(f"Unsupported data-type {args.data_type}")

    data = crawl(spy, args.years)
    print(data)

    # if args.backend == settings.BACKENDS_JSON:
    #     save_to_json(data)
    # elif args.backend == settings.BACKENDS_AIRTABLE:
    #     save_to_airtable(data)
    # else:
    #     raise Exception(f"backend {args.backend} is not supported")


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
