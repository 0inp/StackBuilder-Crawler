import requests
from bs4 import BeautifulSoup

from src.domain.entities import EntryEntity
from src.domain.repositories.entry_repository import EntryRepositoryInterface


class HackerNewsCrawlerEntryAdapter(EntryRepositoryInterface):
    """Crawler implemention for the HackerNews source."""

    @staticmethod
    def get_entry_number_from_html(html) -> int:
        """Get the number of the entry from the html code

        :param html: str
        :return: int
        """
        number = int(html.find("span", class_="rank").get_text().strip("."))
        return number

    @staticmethod
    def get_entry_title_from_html(html) -> str:
        """Get the title of the entry from the html code

        :param html: str
        :return: str
        """
        title = html.find("span", class_="titleline").a.get_text()
        return title

    @staticmethod
    def get_entry_points_from_html(html) -> int | None:
        """Get the number of points of the entry from the html code.
        Might be absent.

        :param html: str
        :return: int | None
        """
        total_points_node = html.next_sibling.find("span", class_="score")
        if total_points_node is None:
            return None
        total_points = int(total_points_node.get_text().strip(" points"))
        return total_points

    @staticmethod
    def get_entry_comments_from_html(html) -> int | None:
        """Get the number of comments of the entry from the html code
        Might be absent

        :param html: str
        :return: int | None
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
        """Get entries from crawling source

        :param source: str
        :param filters: list[str] | None
        :return: list[EntryEntity]
        """
        # TODO: get to page 2 until i get 30 entries
        page = requests.get(source)
        if not page.status_code == 200:
            # TODO: raise exception
            raise
        soup = BeautifulSoup(page.text, "html.parser")
        html_entries = soup.find_all("tr", class_="athing")

        entries = []
        for html_entry in html_entries:
            number = self.get_entry_number_from_html(html_entry)
            title = self.get_entry_title_from_html(html_entry)
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
