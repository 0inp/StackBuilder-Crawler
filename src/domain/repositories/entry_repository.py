from abc import ABC, abstractmethod

from src.domain.entities import EntryEntity


class EntryRepositoryInterface(ABC):
    @abstractmethod
    def get_entries(self, source: str) -> list[EntryEntity]:
        """Get entries from source and apply filters.

        :param source: str
        :return: list[EntryEntity]
        """
        ...
