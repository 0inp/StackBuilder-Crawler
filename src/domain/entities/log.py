from dataclasses import dataclass

from datetime import datetime

from src.domain.dtos.get_entries import Filter, Order


@dataclass
class LogEntity:
    request_time: datetime
    filter: Filter
    order: Order
