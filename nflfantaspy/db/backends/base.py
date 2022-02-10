import abc


class BaseDatabaseClient(abc.ABC):
    @abc.abstractmethod
    def save(self):
        raise NotImplementedError
