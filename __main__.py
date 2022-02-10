import os

from nflfantaspy.db.backends import json
from nflfantaspy.nfl import fantasy
from nflfantaspy.spyder import schedule
from nflfantaspy.parser import schedule, settings

NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
# SEASON_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def main():
    nfl = fantasy.Client(NFL_FF_LEAGUE_ID)
    res = nfl.get_settings(year=2021)
    parser = settings.Parser(res.content)
    context = parser.parse()

    spyder = schedule.Spyder(
        nfl, schedule.Parser, json.DatabaseClient("games.json"), context
    )
    spyder.execute()


if __name__ == "__main__":
    main()
