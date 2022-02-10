from pyairtable.api import Table
from nflfantaspy.db.backends.base import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.table = Table(cfg["api_key"], cfg["base_id"], cfg["table_name"])

    def save(self, payload):
        self.destructive_reset()

        for i, game in enumerate(payload):
            record = {
                "ID": i,
                "Week": game["week"],
                "Home Team": game["home_id"],
                "Away Team": game["away_id"],
                "Home Team Score": game["home_score"],
                "Away Team Score": game["away_score"],
                "Game Type": "REGULAR",
            }
            self.table.create(record)

    def destructive_reset(self):
        ids = []
        for games in self.table.iterate():
            for game in games:
                ids.append(game["id"])
        self.table.batch_delete(ids)
