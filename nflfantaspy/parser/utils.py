from bs4 import Tag


def parse_team_id(tag: Tag, team_id_prefix="teamId-") -> int:
    for cls in tag.attrs["class"]:
        if cls.startswith(team_id_prefix):
            return int(cls.strip(team_id_prefix))

    raise Exception(f"no {team_id_prefix}[0-9]+ class found in {tag}")
