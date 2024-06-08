import pytest

from src.controllers.cli import main
from src.domain.dtos.get_entries import GetEntriesDto
from src.domain.entities.filter import FilterEntity, FilterFieldEnum, FilterOperatorEnum
from src.domain.entities.order import OrderEntity, OrderFieldEnum, OrderDirectionEnum
from src.usecases import GetEntries


class TestCliController:
    @pytest.mark.parametrize(
        ("source", "filter", "order", "verbose", "expected_usecase_dto_params"),
        [
            (
                None,
                None,
                None,
                None,
                GetEntriesDto(
                    source="https://news.ycombinator.com/", filter=None, order=None
                ),
            ),
            (
                "source",
                None,
                None,
                None,
                GetEntriesDto(source="source", filter=None, order=None),
            ),
            (
                None,
                ("number_of_words", "lt", 5),
                None,
                None,
                GetEntriesDto(
                    source="https://news.ycombinator.com/",
                    filter=FilterEntity(
                        field=FilterFieldEnum.number_of_words,
                        operator=FilterOperatorEnum.lt,
                        value=5,
                    ),
                    order=None,
                ),
            ),
            (
                None,
                None,
                ("comments", "desc"),
                None,
                GetEntriesDto(
                    source="https://news.ycombinator.com/",
                    filter=None,
                    order=OrderEntity(
                        field=OrderFieldEnum.comments, direction=OrderDirectionEnum.desc
                    ),
                ),
            ),
            (
                None,
                None,
                None,
                True,
                GetEntriesDto(
                    source="https://news.ycombinator.com/", filter=None, order=None
                ),
            ),
        ],
        ids=[
            "test_without_arguments",
            "test_with_custom_source",
            "test_with_custom_filter",
            "test_with_custom_order",
            "test_verbose",
        ],
    )
    def test_cli_controller(
        self, source, filter, order, verbose, expected_usecase_dto_params, mocker
    ):
        mock_usecase = mocker.patch.object(GetEntries, "execute")
        if source is None:
            main(filter=filter, order=order, verbose=verbose)
        else:
            main(source, filter, order, verbose)
        mock_usecase.assert_called_once_with(dto=expected_usecase_dto_params)
