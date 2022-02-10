from typing import Type

from nflfantaspy.nfl import fantasy
from nflfantaspy.db.backends.base import BaseDatabaseClient
from nflfantaspy.parser.base import BaseParser


class Spyder:
    def __init__(
        self,
        nfl: fantasy.Client,
        parser_class: Type[BaseParser],
        db: BaseDatabaseClient,
        context: dict,
    ):
        self.nfl = nfl
        self.parser_class = parser_class
        self.db = db
        self.context = context

    def execute(self):
        games = []

        for week in range(1, self.context["weeks"] + 1):
            res = self.nfl.get_schedule(year=2021, week=week)
            parser = self.parser_class(res.content)
            games.extend(parser.parse())

        self.db.save(games)
