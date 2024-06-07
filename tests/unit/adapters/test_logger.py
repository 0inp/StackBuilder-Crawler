import logging
from datetime import datetime

import pytest

from src.adapters.logger import LoggerAdapter
from src.domain.entities import (
    FilterEntity,
    FilterFieldEnum,
    FilterOperatorEnum,
    LogEntity,
    OrderDirectionEnum,
    OrderEntity,
    OrderFieldEnum,
)


class TestLoggerAdapter:
    @pytest.fixture
    def log_entity_empty(self):
        entity = LogEntity(request_time=datetime.now(), filter=None, order=None)
        return entity

    @pytest.fixture
    def log_entity_only_filter(self):
        filter_field_enum = FilterFieldEnum.number_of_words
        filter_operator_enum = FilterOperatorEnum.lt
        filter_entity = FilterEntity(
            field=filter_field_enum, operator=filter_operator_enum, value=12
        )

        entity = LogEntity(
            request_time=datetime.now(), filter=filter_entity, order=None
        )
        return entity

    @pytest.fixture
    def log_entity_order_only(self):
        order_field_enum = OrderFieldEnum.comments
        order_direction_enum = OrderDirectionEnum.desc
        order_entity = OrderEntity(
            field=order_field_enum, direction=order_direction_enum
        )

        entity = LogEntity(request_time=datetime.now(), filter=None, order=order_entity)
        return entity

    @pytest.fixture
    def log_entity_full(self):
        filter_field_enum = FilterFieldEnum.number_of_words
        filter_operator_enum = FilterOperatorEnum.lt
        filter_entity = FilterEntity(
            field=filter_field_enum, operator=filter_operator_enum, value=12
        )

        order_field_enum = OrderFieldEnum.comments
        order_direction_enum = OrderDirectionEnum.desc
        order_entity = OrderEntity(
            field=order_field_enum, direction=order_direction_enum
        )

        entity = LogEntity(
            request_time=datetime.now(), filter=filter_entity, order=order_entity
        )
        return entity

    def test_create_logger(self):
        logger = LoggerAdapter(log_level=logging.INFO)
        assert logger is not None
        assert type(logger) == LoggerAdapter
        assert logger.log_level == logging.INFO
        assert logger.logger.level == logging.INFO

    def test_log_debug(self, mocker):
        logger = LoggerAdapter(log_level=logging.DEBUG)
        mock_log_debug = mocker.patch("logging.debug")
        message_log = "message_log"
        logger.log_debug(message_log)
        mock_log_debug.assert_called_once_with(message_log)

    @pytest.mark.parametrize(
        "log_entity,expected",
        [
            (
                "log_entity_empty",
                "Filter by: Nothing - Order by: Nothing",
            ),
            (
                "log_entity_only_filter",
                "Filter by: number_of_words lt 12 - Order by: Nothing",
            ),
            (
                "log_entity_order_only",
                "Filter by: Nothing - Order by: comments desc",
            ),
            (
                "log_entity_full",
                "Filter by: number_of_words lt 12 - Order by: comments desc",
            ),
        ],
    )
    def test_log_request(self, log_entity, expected, request, mocker):
        logger = LoggerAdapter(log_level=logging.DEBUG)
        mock_log_info = mocker.patch.object(logger.logger, "info")
        logger.log_request(request.getfixturevalue(log_entity))
        mock_log_info.assert_called_once_with(expected)
