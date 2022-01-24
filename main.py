import os
from bs4 import BeautifulSoup
import requests


NFL_FF_LEAGUE_PREFIX = "https://fantasy.nfl.com/league"
NFL_FF_LEAGUE_ID = os.environ["NFL_FF_LEAGUE_ID"]
NFL_FF_LEAGUE_URL = f'{NFL_FF_LEAGUE_PREFIX}/{NFL_FF_LEAGUE_ID}'

res = requests.get(NFL_FF_LEAGUE_URL)
res.raise_for_status()

soup = BeautifulSoup(res.content, "html.parser")
print(soup.prettify)