from abc import ABC, abstractmethod

from src.domain.entities import EntryEntity


class EntryRepositoryInterface(ABC):
    """Abstract interface of the Entry repo."""

    @abstractmethod
    def get_entries(self, source: str) -> list[EntryEntity]:
        """Get entries from source and apply filters.

        Args:
            source: str

        Returns:
            entries: list[EntryEntity]
        """
        ...
