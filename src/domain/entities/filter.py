import operator
from dataclasses import dataclass
from enum import Enum


class FilterFieldEnum(Enum):
    """Enum of the field of the filter.

    One of the element of an Entry Entity on which we can apply a filter.

    Attributes:
        index: Filter on the index number.
        title : Filter on the number of words in the title.
        total_points: Filter on the number of points.
        total_comments: Filter on the number of comments.

    """

    index = "index"
    number_of_words = "number_of_words"
    number_of_points = "number_of_points"
    number_of_comments = "number_of_comments"


class FilterOperatorEnum(Enum):
    """Enum of the operator of the filter.

    Attributes:
        lt: Lower than.
        le: Lower than or equal.
        gt: Greater than.
        ge: Greater than or equal.
        eq: Equal to

    """

    lt = "lt"
    le = "le"
    gt = "gt"
    ge = "ge"
    eq = "eq"

    def convert_str_to_operator(self):
        """Returns the operator function according to the enum string."""
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
class FilterEntity:
    """Represents a Filter.

    Attributes:
        field: The field on which the filter will be applied.
        operator: Operator used for the filter.
        value: The value that serves for the filter.

    """

    field: FilterFieldEnum
    operator: FilterOperatorEnum
    value: int
