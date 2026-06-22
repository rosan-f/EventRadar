from abc import ABC, abstractmethod

from event_radar.models import Event


class EventScraper(ABC):
    @abstractmethod
    def scrape(self) -> list[Event]:
        pass