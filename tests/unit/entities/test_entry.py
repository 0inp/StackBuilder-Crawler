from src.domain.entities import EntryEntity


def test_create_entry_entity():
    entity = EntryEntity(
        index=1, title="title", total_points=12, total_comments=13, source="source"
    )
    assert entity is not None
    assert type(entity) == EntryEntity
