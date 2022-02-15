from collections import defaultdict

from nflfantaspy.constants import BRACKET_TYPE_CONSOLATION
from nflfantaspy.fetcher import http
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
        executeCfg = {"bracket_type": BRACKET_TYPE_CONSOLATION}
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
        save_to_airtable(data, {"api_key": args.api_key, "base_id": args.base_id})
    else:
        raise Exception(f"backend {args.cmd} is not supported")


def save_to_json(data: list[dict]):
    db = json.DatabaseClient({"filename": "games.json"})
    db.save(data)


def save_to_airtable(data: list[dict], cfg: dict):
    db = airtable.DatabaseClient(cfg)
    for year, records in data.items():
        db.table = str(year)
        db.save(records)


if __name__ == "__main__":
    main()
