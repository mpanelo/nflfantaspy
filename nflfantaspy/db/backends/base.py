import abc


class BaseDatabaseClient(abc.ABC):
    def __init__(self, cfg: dict):
        self.cfg = cfg

    @abc.abstractmethod
    def save(self):
        raise NotImplementedError
