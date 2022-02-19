import unittest

from nflfantaspy import parser

class TestTeamParser(unittest.TestCase):
    def test_happy_case(self):
        with open("test/html_content/owners.txt", "rb") as f:
            content = f.read()

        parser_teams = parser.Teams(content)
        teams = parser_teams.parse()

        self.assertIsInstance(teams, list)
        for team in teams:
            self.assertIn("id", team)
            self.assertIn("name", team)
            self.assertIn("owner", team)
        
    def test_invalid_content(self):
        parser_teams = parser.Teams(bytes("asdasd", "utf-8"))
        with self.assertRaises(AttributeError):
            parser_teams.parse()