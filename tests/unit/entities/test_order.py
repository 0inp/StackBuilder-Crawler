from src.domain.entities import OrderDirectionEnum, OrderEntity, OrderFieldEnum


def test_create_filter_entity():
    order_field_enum = OrderFieldEnum.comments
    order_direction_enum = OrderDirectionEnum.desc

    entity = OrderEntity(field=order_field_enum, direction=order_direction_enum)
    assert entity is not None
    assert type(entity) == OrderEntity
