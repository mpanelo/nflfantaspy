import os

from nflfantaspy.db.backends import airtable
from nflfantaspy.nfl import fantasy
from nflfantaspy.spyder import schedule as sch
from nflfantaspy.parser import schedule, settings

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
# SEASON_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def main():
    nfl = fantasy.Client(NFL_FF_LEAGUE_ID)
    res = nfl.get_settings(year=2021)
    parser = settings.Parser(res.content)
    context = parser.parse()

    cfg = {
        "api_key": AIRTABLE_API_KEY,
        "base_id": AIRTABLE_BASE_ID,
        "table_name": "Season 2021",
    }
    db = airtable.DatabaseClient(cfg)

    spyder = sch.Spyder(nfl, schedule.Parser, db, context)
    spyder.execute()


if __name__ == "__main__":
    main()
