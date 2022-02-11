from pyairtable.api import Table
from nflfantaspy.db.backends.base import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    def __init__(self, cfg: dict):
        super().__init__(cfg)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, name: str):
        self._table = Table(self.cfg["api_key"], self.cfg["base_id"], name)

    def save(self, records):
        self.destructive_reset()
        self.table.batch_create(records)

    def destructive_reset(self):
        ids = []
        for games in self.table.iterate():
            for game in games:
                ids.append(game["id"])
        self.table.batch_delete(ids)
