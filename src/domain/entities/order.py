from dataclasses import dataclass
from enum import Enum


class OrderFieldEnum(Enum):
    """Enum of the field of the order query.

    One of the element of an Entry Entity on which we can apply an order query.

    Attributes:
        points: Order by the number of points.
        comments: Order by the number of comments.

    """

    points = "points"
    comments = "comments"


class OrderDirectionEnum(Enum):
    """Enum of the direction of the order query.

    Attributes:
        asc: Order ascending.
        desc: Order descending.

    """

    asc = "asc"
    desc = "desc"


@dataclass
class OrderEntity:
    """Represents an Order By query.

    Attributes:
        field: The field on which the order will be applied.
        direction: Desc or Asc.

    """

    field: OrderFieldEnum
    direction: OrderDirectionEnum
