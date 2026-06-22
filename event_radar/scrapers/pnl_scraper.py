import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from event_radar.models import Event
from event_radar.scrapers.base import EventScraper


class PNLScraper(EventScraper):
    BASE_URL = "https://pnl.ac.id"
    NEWS_URL = "https://pnl.ac.id/id/berita"

    DATE_PATTERN = re.compile(
        r"\b(?:0?[1-9]|[12]\d|3[01])\s+"
        r"(?:Januari|Februari|Maret|April|Mei|Juni|Juli|"
        r"Agustus|September|Oktober|November|Desember)\s+"
        r"\d{4}\b",
        re.IGNORECASE,
    )

    def scrape(self) -> list[Event]:
        try:
            response = requests.get(
                self.NEWS_URL,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 EventRadar/0.4 "
                        "Campus Event CLI Tool"
                    )
                },
                timeout=20,
            )

            response.raise_for_status()

        except requests.RequestException as error:
            raise RuntimeError(
                f"Gagal mengambil data dari PNL: {error}"
            ) from error

        soup = BeautifulSoup(response.text, "html.parser")

        events: list[Event] = []
        seen_urls: set[str] = set()

        links = soup.select('a[href*="/id/detail/"]')

        for link in links:
            title = link.get_text(" ", strip=True)
            href = link.get("href")

            if not title or not href:
                continue

            if title.lower() == "selengkapnya":
                continue

            if len(title) < 10:
                continue

            url = urljoin(self.BASE_URL, href)

            if url in seen_urls:
                continue

            category = self._detect_category(title)

            if category is None:
                continue

            date = self._extract_date(link)

            events.append(
                Event(
                    title=title,
                    category=category,
                    date=date,
                    source="pnl",
                    url=url,
                )
            )

            seen_urls.add(url)

        return events

    def _detect_category(self, title: str) -> str | None:
        normalized_title = title.lower()

        category_keywords = {
            "webinar": [
                "webinar",
            ],
            "workshop": [
                "workshop",
                "pelatihan",
            ],
            "lomba": [
                "lomba",
                "kompetisi",
                "competition",
            ],
            "seminar": [
                "seminar",
                "kuliah umum",
            ],
        }

        for category, keywords in category_keywords.items():
            if any(
                keyword in normalized_title
                for keyword in keywords
            ):
                return category

        return None

    def _extract_date(self, link: Tag) -> str:
        current_element: Tag | None = link

        for _ in range(6):
            current_element = current_element.parent

            if current_element is None:
                break

            text = current_element.get_text(
                " ",
                strip=True,
            )

            date_match = self.DATE_PATTERN.search(text)

            if date_match:
                return date_match.group(0)

        return "Tanggal tidak tersedia"