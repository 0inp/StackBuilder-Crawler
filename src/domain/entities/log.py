from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.filter import FilterEntity
from src.domain.entities.order import OrderEntity


@dataclass
class LogEntity:
    """Entity of a Log.

    Attributes:
        request_time (datetime): Timestamp of the log.
        filter (Filter): The Filter entity used by the time of the request.
        order (Order): The Order entity used by the time of the request.

    """

    request_time: datetime
    filter: FilterEntity
    order: OrderEntity
