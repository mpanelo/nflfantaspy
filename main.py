import os
from bs4 import BeautifulSoup
import requests
import re

attr_team_id = re.compile("teamId-[0-9]")

NFL_FF_LEAGUE_PREFIX = "https://fantasy.nfl.com/league"
NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
NFL_FF_LEAGUE_URL = f'{NFL_FF_LEAGUE_PREFIX}/{NFL_FF_LEAGUE_ID}'

TEAM_ID_PREFIX = "teamId-"

def parse_team_id(span):
    for val in span.attrs["class"]:
        if val.startswith(TEAM_ID_PREFIX):
            return val.strip(TEAM_ID_PREFIX)

def main():
    res = requests.get(NFL_FF_LEAGUE_URL)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "html.parser")
    span_tags = soup.find_all("span", attrs={"class": attr_team_id})

    team_ids = set(parse_team_id(span) for span in span_tags)
    print(team_ids)

if __name__ == "__main__":
    main()