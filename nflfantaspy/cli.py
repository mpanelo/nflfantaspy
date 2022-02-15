import argparse
import re

from argparse import ArgumentTypeError


# TODO create constants file
STORAGE_JSON = "json"
STORAGE_AIRTABLE = "airtable"
DATA_TYPE_GAMES = "games"
DATA_TYPE_TEAMS = "teams"


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)

    subparsers = parser.add_subparsers(
        title="storage options", dest="cmd", required=True
    )
    parent = add_shared_arguments()

    add_json_subparser(subparsers, parent)
    add_airtable_subparser(subparsers, parent)
    return parser.parse_args()


def add_json_subparser(subparsers, parent):
    subparsers.add_parser(
        STORAGE_JSON,
        parents=[parent],
        add_help=False,
        description="Store scraped data as a JSON file",
    )


def add_airtable_subparser(subparsers, parent):
    parser_airtable = subparsers.add_parser(
        STORAGE_AIRTABLE,
        parents=[parent],
        add_help=False,
        description="Store scraped data on Airtable",
    )
    parser_airtable.add_argument(
        "--api-key",
        required=True,
        help="Your personal API key to access the Airtable API",
    )
    parser_airtable.add_argument(
        "--base-id",
        required=True,
        help="The ID of the Base containing the tables for the chosen data-type",
    )


def add_shared_arguments():
    parser = argparse.ArgumentParser(
        description="Scrape game and team history from your NFL fantasy football league, and store it as JSON or on Airtable.",
    )
    parser.add_argument(
        "--league-id",
        type=int,
        required=True,
        help="Specify the NFL assigned League ID (check your league settings)",
    )
    parser.add_argument(
        "--years",
        type=parseYears,
        required=True,
        help="Specify a range of years or a year to scrape",
    )
    parser.add_argument(
        "--data-type",
        choices=[DATA_TYPE_GAMES, DATA_TYPE_TEAMS],
        required=True,
        help="Scrappable fantasy football history data types",
    )
    return parser


def parseYears(arg: str):
    m = re.match(r"(\d+)(?:-(\d+))?$", arg)
    if m is None:
        raise ArgumentTypeError(
            f"'{arg}' is not a range of years (examples: '2014-2021' or '2020')"
        )

    start = m.group(1)
    end = m.group(2) or start

    if end < start:
        raise ArgumentTypeError(f"'{arg}' is not an increasing range")

    return list(range(int(start), int(end) + 1))
