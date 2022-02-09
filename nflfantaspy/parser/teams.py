from bs4 import Tag

from nflfantaspy.parser.base import BaseParser
from nflfantaspy.parser import utils


class Parser(BaseParser):
    def parse(self) -> list[dict]:
        tbody = self.soup.find("tbody")
        trs = tbody.find_all("tr")

        teams = []
        for tr in trs:
            teams.append(self._parse_team(tr))
        return teams

    def _parse_team(self, tr: Tag):
        id = utils.parse_team_id(tr, team_id_prefix="team-")

        td = tr.find("td", attrs={"class": "teamOwnerName"})
        span = td.find("span", attrs={"class": "userName"})
        owner = span.get_text().strip().lower()

        td = tr.find("td", attrs={"class": "teamImageAndName"})
        anchor = td.find("a", attrs={"class": "teamName"})
        name = anchor.get_text().strip().lower()

        return {"id": id, "name": name, "owner": owner}
