import logging

from _pytest.scope import HIGH_SCOPES
import pytest

from src.adapters import HackerNewsCrawlerEntryAdapter, FileLoggerAdapter
from src.domain.dtos.get_entries import GetEntriesDto
from src.domain.entities.entry import EntryEntity
from src.domain.entities.filter import FilterEntity, FilterFieldEnum, FilterOperatorEnum
from src.domain.entities.order import OrderDirectionEnum, OrderEntity, OrderFieldEnum
from src.usecases.get_entries_usecase import GetEntries


class TestGetEntriesUsecase:

    def test_get_entries_nominal(self, mocker):
        entries = [
            EntryEntity(
                index=1,
                title="title",
                total_points=12,
                total_comments=12,
                source="source",
            )
        ]
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mocker.patch.object(crawler, "get_entries", return_value=entries)
        mocker.patch.object(logger, "log_debug")
        mocker.patch.object(logger, "log_request")
        usecase = GetEntries(entry_repository=crawler, logger_repository=logger)
        get_entries_dto = GetEntriesDto(source="source", filter=None, order=None)
        result = usecase.execute(dto=get_entries_dto)
        assert result == entries

    def test_get_entries_raise(self, mocker):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mocker.patch.object(crawler, "get_entries", side_effect=Exception)
        mocker.patch.object(logger, "log_debug")
        mocker.patch.object(logger, "log_request")
        usecase = GetEntries(entry_repository=crawler, logger_repository=logger)
        get_entries_dto = GetEntriesDto(source="source", filter=None, order=None)
        with pytest.raises(Exception):
            usecase.execute(dto=get_entries_dto)

    def test_get_entries_filter_number_words_title(self, mocker):
        filtered_entry = EntryEntity(
            index=1,
            title="title",
            total_points=12,
            total_comments=12,
            source="source",
        )
        non_filtered_entry = EntryEntity(
            index=1,
            title="title title",
            total_points=12,
            total_comments=12,
            source="source",
        )
        returned_entries = [filtered_entry, non_filtered_entry]
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mocker.patch.object(crawler, "get_entries", return_value=returned_entries)
        mocker.patch.object(logger, "log_debug")
        mocker.patch.object(logger, "log_request")
        usecase = GetEntries(entry_repository=crawler, logger_repository=logger)
        filter = FilterEntity(
            field=FilterFieldEnum.number_of_words,
            operator=FilterOperatorEnum.gt,
            value=1,
        )
        get_entries_dto = GetEntriesDto(source="source", filter=filter, order=None)
        result = usecase.execute(dto=get_entries_dto)
        assert len(result) == 1
        assert result[0] == non_filtered_entry

    def test_get_entries_order_by_points_desc(self, mocker):
        entry_low_points = EntryEntity(
            index=1,
            title="title",
            total_points=10,
            total_comments=12,
            source="source",
        )
        entry_middle_points = EntryEntity(
            index=1,
            title="title",
            total_points=10,
            total_comments=12,
            source="source",
        )
        entry_high_points = EntryEntity(
            index=1,
            title="title title",
            total_points=100,
            total_comments=12,
            source="source",
        )
        # Random order
        returned_entries = [entry_middle_points, entry_high_points, entry_low_points]
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mocker.patch.object(crawler, "get_entries", return_value=returned_entries)
        mocker.patch.object(logger, "log_debug")
        mocker.patch.object(logger, "log_request")
        usecase = GetEntries(entry_repository=crawler, logger_repository=logger)
        order = OrderEntity(
            field=OrderFieldEnum.points, direction=OrderDirectionEnum.desc
        )
        get_entries_dto = GetEntriesDto(source="source", filter=None, order=order)
        result = usecase.execute(dto=get_entries_dto)
        assert len(result) == len(returned_entries)
        # Assert the result is ordered descending
        assert result == [entry_high_points, entry_middle_points, entry_low_points]
