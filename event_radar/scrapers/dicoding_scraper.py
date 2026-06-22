import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from event_radar.models import Event
from event_radar.scrapers.base import EventScraper


class DicodingScraper(EventScraper):
    BASE_URL = "https://www.dicoding.com"
    EVENTS_URL = "https://www.dicoding.com/events/list"

    DATE_PATTERN = re.compile(
        r"\b(?:0?[1-9]|[12]\d|3[01])\s+"
        r"(?:Januari|Februari|Maret|April|Mei|Juni|Juli|"
        r"Agustus|September|Oktober|November|Desember)\s+"
        r"\d{4}\b",
        re.IGNORECASE,
    )

    EVENT_URL_PATTERN = re.compile(r"/events/\d+")

    def scrape(self) -> list[Event]:
        try:
            response = requests.get(
                self.EVENTS_URL,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 EventRadar/0.5 "
                        "Campus Event CLI Tool"
                    )
                },
                timeout=20,
            )

            response.raise_for_status()

        except requests.RequestException as error:
            raise RuntimeError(
                f"Gagal mengambil data dari Dicoding: {error}"
            ) from error

        soup = BeautifulSoup(response.text, "html.parser")

        events: list[Event] = []
        seen_urls: set[str] = set()

        for link in soup.find_all("a", href=True):
            if not isinstance(link, Tag):
                continue

            href = link.get("href")

            if not isinstance(href, str):
                continue

            if not self.EVENT_URL_PATTERN.search(href):
                continue

            title = self._extract_title(link)

            if not title or len(title) < 10:
                continue

            url = urljoin(self.BASE_URL, href)

            if url in seen_urls:
                continue

            card_text = self._extract_card_text(link)

            events.append(
                Event(
                    title=title,
                    category=self._detect_category(
                        title,
                        card_text,
                    ),
                    date=self._extract_date(card_text),
                    source="dicoding",
                    url=url,
                )
            )

            seen_urls.add(url)

        return events

    def _extract_title(self, link: Tag) -> str:
        title_attribute = link.get("title")

        if isinstance(title_attribute, str):
            title_attribute = title_attribute.strip()

            if title_attribute:
                return title_attribute

        return link.get_text(" ", strip=True)

    def _extract_card_text(self, link: Tag) -> str:
        current_element: Tag | None = link

        for _ in range(7):
            parent = current_element.parent

            if not isinstance(parent, Tag):
                break

            current_element = parent
            text = current_element.get_text(" ", strip=True)

            if "oleh:" in text.lower():
                return text

        return link.get_text(" ", strip=True)

    def _extract_date(self, text: str) -> str:
        date_match = self.DATE_PATTERN.search(text)

        if date_match:
            return date_match.group(0)

        return "Tanggal tidak tersedia"

    def _detect_category(
        self,
        title: str,
        card_text: str,
    ) -> str:
        text = f"{title} {card_text}".lower()

        if "workshop" in text or "pelatihan" in text:
            return "workshop"

        if "webinar" in text:
            return "webinar"

        if any(
            keyword in text
            for keyword in [
                "lomba",
                "kompetisi",
                "competition",
                "challenge",
            ]
        ):
            return "lomba"

        return "seminar"