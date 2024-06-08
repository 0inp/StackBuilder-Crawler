import logging
from dataclasses import dataclass

import pytest
from bs4 import BeautifulSoup, Tag

from src.adapters import HackerNewsCrawlerEntryAdapter, FileLoggerAdapter
from src.domain.entities.entry import EntryEntity


class TestCrawlerAdapter:
    @pytest.fixture
    def html_page(self, request):
        @dataclass
        class HtmlPage:
            text: str
            status_code: int

        with open("./tests/unit/adapters/hn_fixture.html", "r") as file:
            html_page = HtmlPage(text=file.read(), status_code=request.param)
        return html_page

    def test_create_crawler(self):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        assert crawler is not None
        assert type(crawler) == HackerNewsCrawlerEntryAdapter

    @pytest.mark.parametrize("html_page", [200], indirect=True)
    def test_get_entries(self, html_page, mocker):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mock_requests = mocker.patch("requests.get", return_value=html_page)
        source = "source"
        entries = crawler.get_entries(source)
        mock_requests.assert_called_once_with(source)
        expected_first_entry = EntryEntity(
            index=1,
            title="The Backrooms of the Internet Archive",
            total_points=121,
            total_comments=16,
            source=source,
        )
        assert entries[0] == expected_first_entry

    @pytest.mark.parametrize("html_page", [500], indirect=True)
    def test_get_entries_requests_error(self, html_page, mocker):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        mock_requests = mocker.patch("requests.get", return_value=html_page)
        mocker.patch("logging.debug")
        source = "source"
        entries = crawler.get_entries(source)
        mock_requests.assert_called_once_with(source)
        assert entries == []

    @pytest.mark.parametrize(
        "rank_html_string,expected",
        [
            (
                """<td class="title">
                    <span class="rank">12.</span>
                </td>""",
                12,
            ),
            ("", None),
        ],
    )
    def test_get_entry_index_from_html(self, rank_html_string, expected):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        html_string = (
            """<tr class="athing">"""
            f"{rank_html_string}"
            """"<td class="title">
                <span class="titleline"
                ><a href="https://www.fox13seattle.com/news/william-anders-wa-plane-crash">TITLE</a>
                <span class="sitebit comhead">
                    (<a
                    href="https://news.ycombinator.com/from?site=fox13seattle.com"
                    ><span class="sitestr">fox13seattle.com</span></a
                    >)</span>
                </span>
            </td>
        </tr>
        <tr>
            <td class="subtext">
                <span class="subline">
                    <span class="score">351 points</span>
                    by
                    <a href="https://news.ycombinator.com/user?id=TMWNN" class="hnuser">TMWNN</a>
                    <span class="age" title="2024-06-08T00:16:35">
                        <ahref="https://news.ycombinator.com/item?id=40614227">14 hours ago</a>
                    </span>
                    <span id="unv_40614227"></span> |
                    <a href="https://news.ycombinator.com/hide?id=40614227&amp;goto=news">hide</a>
                    |
                    <a href="https://news.ycombinator.com/item?id=40614227">182&nbsp;comments</a>
                </span>
            </td>
        </tr>"""
        )
        soup = BeautifulSoup(html_string, "html.parser")
        html_entries = soup.find_all("tr", class_="athing")
        index = crawler.get_entry_index_from_html(html_entries[0])
        assert index == expected

    @pytest.mark.parametrize(
        "title_html_string,expected",
        [
            (
                """<td class="title">
                   <span class="titleline"><a href="link">TITLE</a>
                   <span class="sitebit comhead">
                       (<a
                       href="https://news.ycombinator.com/from?site=fox13seattle.com"
                       ><span class="sitestr">fox13seattle.com</span></a
                       >)</span>
                   </span>
                </td>""",
                "TITLE",
            ),
            ("", None),
        ],
    )
    def test_get_entry_title_from_html(self, title_html_string, expected):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        html_string = (
            """<tr class="athing"><td class="title"><span class="rank">12.</span></td>"""
            f"{title_html_string}"
            """"
        </tr>
        <tr>
            <td class="subtext">
                <span class="subline">
                    <span class="score">351 points</span>
                    by
                    <a href="https://news.ycombinator.com/user?id=TMWNN" class="hnuser">TMWNN</a>
                    <span class="age" title="2024-06-08T00:16:35">
                        <ahref="https://news.ycombinator.com/item?id=40614227">14 hours ago</a>
                    </span>
                    <span id="unv_40614227"></span> |
                    <a href="https://news.ycombinator.com/hide?id=40614227&amp;goto=news">hide</a>
                    |
                    <a href="https://news.ycombinator.com/item?id=40614227">182&nbsp;comments</a>
                </span>
            </td>
        </tr>"""
        )
        soup = BeautifulSoup(html_string, "html.parser")
        html_entries = soup.find_all("tr", class_="athing")
        title = crawler.get_entry_title_from_html(html_entries[0])
        assert title == expected

    @pytest.mark.parametrize(
        "points_html_string,expected",
        [
            (
                """<span class="score">351 points</span>""",
                351,
            ),
            ("", None),
        ],
    )
    @pytest.mark.skip(
        reason="Can't make html string to get html.next_sibling. Problem with newline char"
    )
    def test_get_entry_points_from_html(self, points_html_string, expected):
        logger = FileLoggerAdapter(log_level=logging.INFO)
        crawler = HackerNewsCrawlerEntryAdapter(logger=logger)
        html_string = (
            """
                <tr class="athing">
                    <td class="title">
                        <span class="rank">12.</span>
                    </td>
                    <td class="title">
                        <span class="titleline"><a href="https://www.fox13seattle.com/news/william-anders-wa-plane-crash">TITLE</a>
                        <span class="sitebit comhead">
                            (<a
                            href="https://news.ycombinator.com/from?site=fox13seattle.com"
                            ><span class="sitestr">fox13seattle.com</span></a
                            >)</span>
                        </span>
                    </td>
                </tr>
                <tr>
                    <td class="subtext">
                        <span class="subline">
            """
            f"{points_html_string}"
            """
                        by
                        <a href="https://news.ycombinator.com/user?id=TMWNN" class="hnuser">TMWNN</a>
                        <span class="age" title="2024-06-08T00:16:35">
                            <ahref="https://news.ycombinator.com/item?id=40614227">14 hours ago</a>
                        </span>
                        <span id="unv_40614227"></span> |
                        <a href="https://news.ycombinator.com/hide?id=40614227&amp;goto=news">hide</a>
                        |
                        <a href="https://news.ycombinator.com/item?id=40614227">182&nbsp;comments</a>
                    </span>
                </td>
            </tr>
            """
        )
        soup = BeautifulSoup(html_string.replace("\n", " "), "html.parser")
        html_entries = soup.find_all("tr", class_="athing")
        points = crawler.get_entry_points_from_html(html_entries[0])
        assert points == expected
