import operator

from src.domain.entities import FilterEntity, FilterFieldEnum, FilterOperatorEnum


def test_create_filter_entity():
    filter_field_enum = FilterFieldEnum.number_of_words
    filter_operator_enum = FilterOperatorEnum.lt

    entity = FilterEntity(
        field=filter_field_enum, operator=filter_operator_enum, value=12
    )
    assert entity is not None
    assert type(entity) == FilterEntity


def test_filter_operator_convert():
    filter_operator_enum = FilterOperatorEnum.lt
    filter_operator = filter_operator_enum.convert_str_to_operator()

    assert filter_operator == operator.lt
