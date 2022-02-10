import json
import os

from nflfantaspy.db.backends.base import BaseDatabaseClient

ROOT_DIR = "data/"


class DatabaseClient(BaseDatabaseClient):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, payload: dict):
        with open(os.path.join(ROOT_DIR, self.filename), "w") as f:
            json.dump(payload, f, indent=4, sort_keys=True)

    def load(self):
        with open(os.path.join(ROOT_DIR, self.filename), "r") as f:
            return json.load(f)
