import os
import repo

from models import League
from pyairtable.api import Table

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

# Table(AIRTABLE_API_KEY, )
table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Teams")

# clear records in table
team_ids = []
for teams in table.iterate():
    for team in teams:
        team_ids.append(team["id"])
table.batch_delete(team_ids)

league = repo.read("league.json", League)

teams_by_id = {}
for season in league.seasons:
    for team in season.teams:
        teams_by_id[team.nfl_id] = team

# create records in table
sorted_teams = sorted(teams_by_id.items())
teams_records = []
for _, team in sorted_teams:
    teams_records.append(
        table.create({"ID": team.nfl_id, "Name": team.name, "Owner": team.owner})
    )

# create team NFL ID to record ID
record_id = {}
for record in teams_records:
    nfl_id = record["fields"]["ID"]
    record_id[nfl_id] = record["id"]

table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Season 2021")

# clear records in Season 2021
game_ids = []
for games in table.iterate():
    for game in games:
        game_ids.append(game["id"])
table.batch_delete(game_ids)

for season in league.seasons:
    if season.year != 2021:
        continue

    for i, game in enumerate(season.games):
        record = {
            "ID": i,
            "Week": game.week,
            "Home Team": [record_id[game.home_id]],
            "Away Team": [record_id[game.away_id]],
            "Home Team Score": game.home_score,
            "Away Team Score": game.away_score,
            "Game Type": game.type,
        }
        table.create(record)
