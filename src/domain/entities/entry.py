from dataclasses import dataclass


@dataclass
class EntryEntity:
    number: int
    title: str
    total_points: int
    total_comments: int
    source: str
