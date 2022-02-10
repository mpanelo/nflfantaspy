import abc
from bs4 import BeautifulSoup


class BaseParser(abc.ABC):
    def __init__(self, content: bytes):
        self.soup = BeautifulSoup(content, "html.parser")

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError
