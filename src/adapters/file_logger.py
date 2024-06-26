import logging

from src.domain.entities import LogEntity
from src.domain.repositories import LogRepositoryInterface


class FileLoggerAdapter(LogRepositoryInterface):
    """File Logger implementation.

    This logger will log everything according to the log level passed
    in a file called app.log.

    """

    def __init__(self, log_level: int):
        self.log_level = log_level
        self.logger = logging.getLogger("adapter_logger")
        logging.basicConfig(
            filename="./data/app.log",
            filemode="a",
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(levelname)s - %(asctime)-s - %(message)s",
        )
        self.logger.setLevel(self.log_level)

    def log_request(self, log_entity: LogEntity):
        if log_entity.filter is None:
            filter_log = "Nothing"
        else:
            filter_log = f"{log_entity.filter.field.value} {log_entity.filter.operator.value} {log_entity.filter.value}"
        if log_entity.order is None:
            order_log = "Nothing"
        else:
            order_log = (
                f"{log_entity.order.field.value} {log_entity.order.direction.value}"
            )
        log_message = f"Filter by: {filter_log} - Order by: {order_log}"
        self.logger.info(log_message)

    def log_debug(self, message: str) -> None:
        logging.debug(message)
