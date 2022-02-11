import requests


def get(url: str, params: dict = None) -> bytes:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.content
