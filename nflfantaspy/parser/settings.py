import re
from nflfantaspy.parser.base import BaseParser

DIGIT_REGEX = re.compile("\d+")


class Parser(BaseParser):
    def parse(self):
        playoff_weeks = self._parse_playoff_weeks()
        return {"weeks": playoff_weeks[-1], "playoff_weeks": playoff_weeks}

    def _parse_playoff_weeks(self):
        tag = self.soup.find("em", string="Playoffs")
        div = tag.next_sibling
        text = div.string

        playoff_weeks, _ = text.strip().split("-")
        matches = DIGIT_REGEX.findall(playoff_weeks)

        return [int(match) for match in matches]
