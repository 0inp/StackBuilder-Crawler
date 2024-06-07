import logging
from dataclasses import dataclass
from typing import Optional

import typer
from typing_extensions import Annotated

from src.adapters import CrawlerEntryAdapter, LoggerAdapter
from src.domain.dtos.get_entries import (
    Filter,
    FilterFieldEnum,
    FilterOperatorEnum,
    GetEntriesDto,
    Order,
    OrderDirectionEnum,
    OrderFieldEnum,
)
from src.usecases import GetEntries


@dataclass
class CliController:
    source: str
    filter: Filter | None
    order: Order | None
    verbose: bool

    def run(self):
        crawler_repo = CrawlerEntryAdapter()

        log_level = logging.INFO
        if self.verbose:
            log_level = logging.DEBUG
        logger_repo = LoggerAdapter(log_level=log_level)

        dto = GetEntriesDto(source=self.source, filter=self.filter, order=self.order)
        result_entries = GetEntries(crawler_repo, logger_repo).execute(dto=dto)

        typer.echo("---RESULT---")
        for entry in result_entries:
            typer.echo(entry)


def main(
    source: Annotated[
        str, typer.Argument(help="Source to get entries", show_default=True)
    ] = "https://news.ycombinator.com/",
    filter: Annotated[
        Optional[tuple[FilterFieldEnum, FilterOperatorEnum, int]],
        typer.Option(
            help="Options for the filter (ex titles with more than 5 words: number_of_words lt 5)",
            show_default=False,
        ),
    ] = None,
    order: Annotated[
        Optional[tuple[OrderFieldEnum, OrderDirectionEnum]],
        typer.Option(
            help="Options for the order (ex order by points desc: number_of_points desc)",
            show_default=False,
        ),
    ] = None,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="If True, set Log Level to DEBUG"
    ),
):

    filter_cls = None
    if filter is not None:
        filter_field, operator, value = filter
        filter_cls = Filter(field=filter_field, operator=operator, value=value)
    order_cls = None
    if order is not None:
        order_field, direction = order
        order_cls = Order(field=order_field, direction=direction)
    CliController(
        source=source, filter=filter_cls, order=order_cls, verbose=verbose
    ).run()
