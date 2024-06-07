from abc import ABC, abstractmethod

from src.domain.entities import LogEntity


class LogRepositoryInterface(ABC):
    log_level: bool

    @abstractmethod
    def log_request(self, log_entity: LogEntity):
        """Log the request.

        :param log_entity: LogEntity
        :return:
        """
        ...
