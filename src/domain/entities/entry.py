from dataclasses import dataclass


@dataclass
class EntryEntity:
    index: int
    title: str
    total_points: int
    total_comments: int
    source: str
