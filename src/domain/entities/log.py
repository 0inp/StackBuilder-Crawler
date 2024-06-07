from dataclasses import dataclass

from datetime import datetime

from src.domain.entities.filter import FilterEntity
from src.domain.entities.order import OrderEntity


@dataclass
class LogEntity:
    request_time: datetime
    filter: FilterEntity
    order: OrderEntity
