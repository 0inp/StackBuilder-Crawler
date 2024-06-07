from datetime import datetime
from src.domain.entities import (
    LogEntity,
    FilterEntity,
    OrderEntity,
    FilterFieldEnum,
    FilterOperatorEnum,
    OrderFieldEnum,
    OrderDirectionEnum,
)


def test_create_log_entity():
    filter_field_enum = FilterFieldEnum.number_of_words
    filter_operator_enum = FilterOperatorEnum.lt
    filter_entity = FilterEntity(
        field=filter_field_enum, operator=filter_operator_enum, value=12
    )

    order_field_enum = OrderFieldEnum.comments
    order_direction_enum = OrderDirectionEnum.desc
    order_entity = OrderEntity(field=order_field_enum, direction=order_direction_enum)

    entity = LogEntity(
        request_time=datetime.now(), filter=filter_entity, order=order_entity
    )
    assert entity is not None
    assert type(entity) == LogEntity
