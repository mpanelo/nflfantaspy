import os
import repo

from models import League
from pyairtable.api import Table

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

# Table(AIRTABLE_API_KEY, )
table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Teams")

# clear records in table
game_ids = []
for games in table.iterate():
    for game in games:
        game_ids.append(game["id"])
table.batch_delete(game_ids)

league = repo.read("league.json", League)

teams_by_id = {}
for season in league.seasons:
    for team in season.teams:
        teams_by_id[team.nfl_id] = team

# create records in table
sorted_teams = sorted(teams_by_id.items())
for _, team in sorted_teams:
    print(table.create({"ID": team.nfl_id, "Name": team.name, "Owner": team.owner}))