from event_radar.models import Event
from event_radar.scrapers.base import EventScraper


class PNLScraper(EventScraper):
    def scrape(self) -> list[Event]:
        return [
            Event(
                title="Seminar Nasional Cybersecurity",
                category="seminar",
                date="30 Juni 2026",
                source="pnl",
                url="https://example.com/pnl/seminar-cybersecurity",
            ),
            Event(
                title="Lomba UI/UX Mahasiswa",
                category="lomba",
                date="12 Juli 2026",
                source="pnl",
                url="https://example.com/pnl/lomba-ui-ux",
            ),
        ]