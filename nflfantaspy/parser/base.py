from bs4 import BeautifulSoup


class BaseParser:
    def __init__(self, content: bytes):
        self.soup = BeautifulSoup(content, "html.parser")
