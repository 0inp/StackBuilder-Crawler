from datetime import datetime
import logging
import sqlite3

from src.domain.entities import LogEntity
from src.domain.repositories import LogRepositoryInterface


class DBLoggerAdapter(LogRepositoryInterface):
    """SQLite DB Logger implementation.

    This logger will log the request information in a SQLite database.

    """

    def __init__(self, log_level: int):
        self.log_level = log_level
        self.con = sqlite3.connect("data/app.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS log_request(
                request_time TEXT,
                filter_field TEXT,
                filter_operator TEXT,
                filter_value INT,
                order_field TEXT,
                order_direction TEXT
            )
        """
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS log_debug(
                debug_time TEXT,
                message TEXT
            )
            """
        )

    def log_request(self, log_entity: LogEntity):
        log_filter_data = (None, None, None)
        if log_entity.filter is not None:
            log_filter_data = (
                log_entity.filter.field.value,
                log_entity.filter.operator.value,
                log_entity.filter.value,
            )
        log_order_data = (None, None)
        if log_entity.order is not None:
            log_order_data = (
                log_entity.order.field.value,
                log_entity.order.direction.value,
            )
        log_data = (log_entity.request_time,)
        log_data += log_filter_data
        log_data += log_order_data
        self.cur.execute(
            """
                INSERT INTO log_request VALUES
                (?, ?, ?, ?, ?, ?)
            """,
            log_data,
        )
        self.con.commit()

    def log_debug(self, message: str) -> None:
        if self.log_level >= logging.DEBUG:
            self.cur.execute(
                """
                    INSERT INTO log_debug VALUES
                    (?, ?)
                """,
                (datetime.now(), message),
            )
