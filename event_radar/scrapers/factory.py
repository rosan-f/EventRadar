from event_radar.scrapers.base import EventScraper
from event_radar.scrapers.dicoding_scraper import DicodingScraper
from event_radar.scrapers.pnl_scraper import PNLScraper


class ScraperFactory:
    _scrapers: dict[str, type[EventScraper]] = {
        "pnl": PNLScraper,
        "dicoding": DicodingScraper,
    }

    @classmethod
    def create(cls, source: str) -> EventScraper:
        scraper_class = cls._scrapers.get(source.lower())

        if scraper_class is None:
            raise ValueError(
                f"Sumber '{source}' tidak tersedia."
            )

        return scraper_class()

    @classmethod
    def create_all(cls) -> list[EventScraper]:
        return [
            scraper_class()
            for scraper_class in cls._scrapers.values()
        ]