import logging
from dataclasses import dataclass
from typing import Optional

import typer
from typing_extensions import Annotated

from src.adapters import (
    HackerNewsCrawlerEntryAdapter,
    FileLoggerAdapter,
    DBLoggerAdapter,
)
from src.domain.dtos.get_entries import (
    GetEntriesDto,
)
from src.domain.entities import (
    FilterEntity,
    FilterFieldEnum,
    FilterOperatorEnum,
    OrderDirectionEnum,
    OrderEntity,
    OrderFieldEnum,
)
from src.domain.entities.entry import EntryEntity
from src.usecases import GetEntries


@dataclass
class CliController:
    """CLI controller of the application."""

    @staticmethod
    def print_entry_output(entry: EntryEntity):
        output_string = f"{entry.index}. {entry.title} | Total Points : {entry.total_points} | Total Comments : {entry.total_comments}"
        typer.echo(output_string)

    def run(
        self,
        source: str,
        filter: FilterEntity | None,
        order: OrderEntity | None,
        log_in_db: bool,
        verbose: bool,
    ):
        """Call the GetEntries usecase.

        Print in the console the output
        Args
            source (str): url of the source to use.
            filter (Optional(FilterEntity)): Representation of a filter to use if there is one.
            order (Optional(OrderEntity)): Representation of an order query to use if there is one.
            log_in_db (bool): DbLogger if True else FileLogger
            verbose (bool): LogLevel.DEBUG if verbose is True, else LogLevel.INFO

        """
        log_level = logging.INFO
        if verbose:
            log_level = logging.DEBUG
        logger_repo = FileLoggerAdapter(log_level=log_level)
        if log_in_db:
            logger_repo = DBLoggerAdapter(log_level=log_level)

        # TODO: if not source == "HackerNews" then use Default Crawler
        crawler_repo = HackerNewsCrawlerEntryAdapter(logger=logger_repo)

        dto = GetEntriesDto(source=source, filter=filter, order=order)
        result_entries = GetEntries(crawler_repo, logger_repo).execute(dto=dto)

        typer.echo(f"---RESULT FROM SOURCE : {source}---")
        for entry in result_entries:
            self.print_entry_output(entry)


def main(
    source: Annotated[
        str, typer.Argument(help="Source to get entries", show_default=True)
    ] = "https://news.ycombinator.com/",
    filter: Annotated[
        Optional[tuple[FilterFieldEnum, FilterOperatorEnum, int]],
        typer.Option(
            "--filter",
            "-f",
            help="Options for the filter (ex titles with more than 5 words: number_of_words lt 5)",
            show_default=False,
        ),
    ] = None,
    order: Annotated[
        Optional[tuple[OrderFieldEnum, OrderDirectionEnum]],
        typer.Option(
            "--order",
            "-o",
            help="Options for the order (ex order by points desc: number_of_points desc)",
            show_default=False,
        ),
    ] = None,
    log_in_db: bool = typer.Option(
        False, "--db-log", "-d", help="If True, log in a SQLite db"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="If True, set Log Level to DEBUG"
    ),
):
    """CLI entrypoint.

    Print in the console the output
    Args
        source (str): url of the source to use.
        filter (Optional(FilterEntity)): Representation of a filter to use if there is one.
        order (Optional(OrderEntity)): Representation of an order query to use if there is one.
        log_in_db (bool): DbLogger if True else FileLogger
        verbose (bool): LogLevel.DEBUG if verbose is True, else LogLevel.INFO

    """

    filter_cls = None
    if filter is not None:
        filter_field, operator, value = filter
        filter_cls = FilterEntity(
            field=filter_field,
            operator=operator,
            value=value,
        )
    order_cls = None
    if order is not None:
        order_field, direction = order
        order_cls = OrderEntity(field=order_field, direction=direction)
    CliController().run(
        source=source,
        filter=filter_cls,
        order=order_cls,
        log_in_db=log_in_db,
        verbose=verbose,
    )
