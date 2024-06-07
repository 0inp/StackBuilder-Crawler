# from datetime import datetime
# from src.domain.repositories import (
#     EntryRepository,
#     LoggerRepository,
# )
from src.domain.dtos.get_entries import (
    Filter,
    Order,
    FilterFieldEnum,
    FilterOperatorEnum,
    OrderFieldEnum,
    OrderDirectionEnum,
    GetEntriesDto,
)
from src.domain.repositories import (
    EntryRepositoryInterface,
)

# from src.domain.entities import EntryEntity, LogEntity
from src.domain.entities import EntryEntity


class GetEntries:
    # def __init__(
    #     self, entry_repository: EntryRepository, logger_repository: LoggerRepository
    # ) -> None:
    def __init__(self, entry_repository: EntryRepositoryInterface) -> None:
        self.entry_repository = entry_repository

    # self.logger_repository = logger_repository

    @staticmethod
    def filter_entries(
        entries: list[EntryEntity],
        filter: Filter,
    ) -> list[EntryEntity]:
        match filter.field:
            case FilterFieldEnum.number:
                operator_func = filter.operator.convert_str_to_operator()
                filtered_entries = [
                    entry
                    for entry in entries
                    if operator_func(entry.number, filter.value)
                ]
            case FilterFieldEnum.number_of_words:
                operator_func = filter.operator.convert_str_to_operator()
                filtered_entries = [
                    entry
                    for entry in entries
                    if operator_func(len(entry.title.split()), filter.value)
                ]
            case FilterFieldEnum.number_of_points:
                operator_func = filter.operator.convert_str_to_operator()
                filtered_entries = [
                    entry
                    for entry in entries
                    if operator_func(entry.total_points, filter.value)
                ]
            case FilterFieldEnum.number_of_comments:
                operator_func = filter.operator.convert_str_to_operator()
                filtered_entries = [
                    entry
                    for entry in entries
                    if operator_func(entry.total_comments, filter.value)
                ]
        return filtered_entries

    @staticmethod
    def order_entries(entries: list[EntryEntity], order: Order) -> list[EntryEntity]:
        print(order.direction)
        reverse = True if order.direction == OrderDirectionEnum.desc else False
        print(reverse)
        match order.field:
            case OrderFieldEnum.points:
                ordered_entries = sorted(
                    entries, key=lambda x: x.total_points, reverse=reverse
                )
            case OrderFieldEnum.comments:
                ordered_entries = sorted(
                    entries, key=lambda x: x.total_comments, reverse=reverse
                )
        return ordered_entries

    def execute(self, dto: GetEntriesDto) -> list[EntryEntity]:
        # Get all entries
        entries = []
        try:
            entries = self.entry_repository.get_entries(source=dto.source)
        except Exception as exception:
            raise exception

        # Filter entries
        filtered_entries = entries
        if dto.filter is not None:
            filtered_entries = self.filter_entries(entries, dto.filter)

        # Order entries
        ordered_entries = filtered_entries
        if dto.order is not None:
            ordered_entries = self.order_entries(filtered_entries, dto.order)
        # log = LogEntity(request_time=datetime.now(), filters=[])
        # try:
        #     self.logger_repository.log_request(log)
        # except Exception as exception:
        #     raise exception
        return ordered_entries