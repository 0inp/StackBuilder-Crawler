from abc import ABC, abstractmethod

from src.domain.entities import LogEntity


class LogRepositoryInterface(ABC):
    """Abstract interface of the repository repo.

    Attributes:
        log_level (int): Level of logging (INFO, DEBUG, etc).

    """

    def __init__(self, log_level: int):
        self.log_level = log_level

    @abstractmethod
    def log_request(self, log_entity: LogEntity):
        """Log the request.

        Args:
            log_entity (LogEntity): Entity with all the informations for logging.

        """
        ...
