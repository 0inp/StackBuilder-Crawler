import logging

from src.domain.entities import LogEntity
from src.domain.repositories import LogRepositoryInterface


class LoggerAdapter(LogRepositoryInterface):
    """Crawler Repository for Entries"""

    def __init__(self, log_level: bool):
        logging.basicConfig(
            filename="app.log",
            filemode="a",
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(levelname)s - %(asctime)-s - %(message)s",
            level=log_level,
        )
        self.logger = logging.getLogger(__name__)

    def log_request(self, log: LogEntity):

        filter_log = (
            f"{log.filter.field.value} {log.filter.operator.value} {log.filter.value}"
        )
        order_log = f"{log.order.field.value} {log.order.direction.value}"
        log_message = f"Filter by: {filter_log} - Order by: {order_log}"
        self.logger.info(log_message)

    def log_debug(self, message: str) -> None:
        """Log debug message.
        :param message: Message to log.
        """
        logging.debug(message)
