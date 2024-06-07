import operator
from dataclasses import dataclass
from enum import Enum, auto


class FilterFieldEnum(Enum):
    number = "number"
    number_of_words = "number_of_words"
    number_of_points = "number_of_points"
    number_of_comments = "number_of_comments"


class FilterOperatorEnum(Enum):
    lt = "lt"
    le = "le"
    gt = "gt"
    ge = "ge"
    eq = "eq"

    def convert_str_to_operator(self):
        match self.value:
            case "lt":
                return operator.lt
            case "le":
                return operator.le
            case "gt":
                return operator.gt
            case "ge":
                return operator.ge
            case "eq":
                return operator.eq


@dataclass
class Filter:
    field: FilterFieldEnum
    operator: FilterOperatorEnum
    value: int


class OrderFieldEnum(Enum):
    points = "points"
    comments = "comments"


class OrderDirectionEnum(Enum):
    asc = "asc"
    desc = "desc"


@dataclass
class Order:
    field: OrderFieldEnum
    direction: OrderDirectionEnum


@dataclass
class GetEntriesDto:
    source: str
    filter: Filter | None
    order: Order | None
