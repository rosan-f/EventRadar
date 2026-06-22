from event_radar.models import Event
from event_radar.scrapers.base import EventScraper


class HimatikScraper(EventScraper):
    def scrape(self) -> list[Event]:
        return [
            Event(
                title="Workshop Python untuk Pemula",
                category="workshop",
                date="5 Juli 2026",
                source="himatik",
                url="https://example.com/himatik/workshop-python",
            ),
            Event(
                title="Webinar Karier di Bidang Teknologi",
                category="webinar",
                date="18 Juli 2026",
                source="himatik",
                url="https://example.com/himatik/webinar-karier",
            ),
        ]