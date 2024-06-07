from dataclasses import dataclass


@dataclass
class EntryEntity:
    """Entity of an Entry.

    Attributes:
        index (int): Index of the entry according to the source.
        title (str): The title of the entry.
        total_points (int): The number of points of the entry (~upvotes).
        total_comments (int): The number of comments of the entry.
        source (str): The url of the source of the entry.

    """

    index: int
    title: str
    total_points: int
    total_comments: int
    source: str
