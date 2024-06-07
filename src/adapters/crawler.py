import requests
from bs4 import BeautifulSoup, Tag

from src.domain.entities import EntryEntity
from src.domain.repositories.entry_repository import EntryRepositoryInterface


class HackerNewsCrawlerEntryAdapter(EntryRepositoryInterface):
    """Crawler implemention for the HackerNews source."""

    @staticmethod
    def get_entry_index_from_html(html: Tag) -> int | None:
        """Get the index of the entry from the html code.

        Args
            html (Tag): represent an entry node in the html.

        Returns:
            index (Optional(int)): the index of the entry.
        """
        html_rank = html.find("span", class_="rank")
        try:
            index = int(html_rank.get_text().strip("."))
        except AttributeError:
            return None
        return index

    @staticmethod
    def get_entry_title_from_html(html: Tag) -> str | None:
        """Get the title of the entry from the html code.

        Args
            html (Tag): represent an entry node in the html.

        Returns:
            title (Optional(str)): the title of the entry.

        """
        html_titleline = html.find("span", class_="titleline")
        try:
            title = html_titleline.a.get_text()
        except AttributeError:
            return None
        return title

    @staticmethod
    def get_entry_points_from_html(html: Tag) -> int | None:
        """Get the number of points of the entry from the html code.

        Args
            html (Tag): represent an entry node in the html.

        Returns:
            total_points (Optional(int)): number of points of an entry if found.

        """
        try:
            total_points_node = html.next_sibling.find("span", class_="score")
            total_points = int(total_points_node.get_text().strip(" points"))
        except AttributeError:
            return None
        return total_points

    @staticmethod
    def get_entry_comments_from_html(html: Tag) -> int | None:
        """Get the number of comments of the entry from the html code.

        Manage the case with 0 comments.

        Args
            html (Tag): represent an entry node in the html.

        Returns:
            total_comments (Optional(int)): number of comments of an entry if found.

        """
        subline_nodes = html.next_sibling.find_all("a")

        # Check if string is present in each string in the list using enumerate
        for item in subline_nodes:
            node_text = item.get_text()
            if isinstance(node_text, str) and "comment" in node_text:
                total_comments = int(node_text.split()[0])
                return total_comments
            if isinstance(node_text, str) and "discuss" in node_text:
                return 0
        return None

    def get_entries(self, source: str) -> list[EntryEntity]:
        # TODO: get to page 2 until i get 30 entries
        page = requests.get(source)
        if not page.status_code == 200:
            # TODO: raise exception
            raise
        soup = BeautifulSoup(page.text, "html.parser")
        html_entries = soup.find_all("tr", class_="athing")

        entries = []
        for html_entry in html_entries:
            index = self.get_entry_index_from_html(html_entry)
            if index is None:
                continue
            title = self.get_entry_title_from_html(html_entry)
            if title is None:
                continue
            total_points = self.get_entry_points_from_html(html_entry)
            if total_points is None:
                continue
            total_comments = self.get_entry_comments_from_html(html_entry)
            if total_comments is None:
                continue
            entry = EntryEntity(
                index=number,
                title=title,
                total_points=total_points,
                total_comments=total_comments,
                source=source,
            )
            entries.append(entry)

        return entries
