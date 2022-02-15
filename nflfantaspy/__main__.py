from collections import defaultdict

from nflfantaspy.fetcher import http
from nflfantaspy import settings
from nflfantaspy import parser
from nflfantaspy import spyder
from nflfantaspy.db.backends import airtable, json
from nflfantaspy import cli


def main():
    args = cli.parse_args()
    executeCfg = {}

    if args.data_type == cli.DATA_TYPE_GAMES:
        schedule = spyder.Schedule(args.league_id, http.get, parser.Schedule)
        playoffs = spyder.Playoffs(args.league_id, http.get, parser.Playoffs)
        spy = spyder.Games(schedule=schedule, playoffs=playoffs)
        # bracket_type choices: championship, consolation
        executeCfg = {"bracket_type": "championship"}
    elif args.data_type == cli.DATA_TYPE_TEAMS:
        spy = spyder.Teams(args.league_id, http.get, parser.Teams)
    else:
        raise Exception(f"Unsupported data-type {args.data_type}")

    data = defaultdict(list)
    for year in args.years:
        executeCfg["year"] = year
        data[year] = spy.execute(**executeCfg)

    if args.cmd == cli.STORAGE_JSON:
        save_to_json(data)
    elif args.cmd == cli.STORAGE_AIRTABLE:
        save_to_airtable(data)
    else:
        raise Exception(f"backend {args.cmd} is not supported")


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


if __name__ == "__main__":
    main()
