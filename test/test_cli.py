import contextlib
import io
import unittest

from nflfantaspy import cli


class TestCLI(unittest.TestCase):
    def test_happy_case(self):
        args = cli.parse_args(
            ["json", "--years", "2021", "--data-type", "games", "--league-id", "1"]
        )
        self.assertEqual(args.cmd, "json")
        self.assertEqual(args.years, [2021])
        self.assertEqual(args.data_type, "games")
        self.assertEqual(args.league_id, 1)

    def test_league_id_not_given(self):
        f = io.StringIO()

        with self.assertRaises(SystemExit) as e, contextlib.redirect_stderr(f):
            cli.parse_args(["json", "--years", "2021", "--data-type", "games"])
        self.assertEqual(e.exception.code, 2)
        self.assertTrue(
            "nflfantaspy json: error: the following arguments are required: --league-id"
            in f.getvalue()
        )

    def test_invalid_years_range(self):
        f = io.StringIO()

        with self.assertRaises(SystemExit) as e, contextlib.redirect_stderr(f):
            cli.parse_args(
                [
                    "json",
                    "--years",
                    "2021-2",
                    "--data-type",
                    "games",
                    "--league-id",
                    "1",
                ]
            )
        self.assertEqual(e.exception.code, 2)
        self.assertTrue(
            "nflfantaspy json: error: argument --years: '2021-2' is not an increasing range"
            in f.getvalue()
        )

    def test_unsupported_data_type(self):
        f = io.StringIO()

        with self.assertRaises(SystemExit) as e, contextlib.redirect_stderr(f):
            cli.parse_args(
                [
                    "json",
                    "--years",
                    "2018-2020",
                    "--data-type",
                    "btc",
                    "--league-id",
                    "1",
                ]
            )

        self.assertEqual(e.exception.code, 2)
        self.assertTrue(
            "nflfantaspy json: error: argument --data-type: invalid choice: 'btc' (choose from 'games', 'teams')"
            in f.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
