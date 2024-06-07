from dataclasses import dataclass

from src.domain.entities import FilterEntity, OrderEntity


@dataclass
class GetEntriesDto:
    source: str
    filter: FilterEntity | None
    order: OrderEntity | None
