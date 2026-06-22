import argparse

from event_radar.formatter import display_events
from event_radar.models import Event
from event_radar.scrapers.himatik_scraper import HimatikScraper
from event_radar.scrapers.pnl_scraper import PNLScraper


APP_NAME = "EventRadar"
APP_VERSION = "0.2.0"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="event-radar",
        description=(
            "CLI tool untuk mengambil dan menampilkan "
            "informasi seminar, workshop, lomba, dan webinar."
        ),
    )

    parser.add_argument(
        "--source",
        choices=["pnl", "himatik", "all"],
        default="all",
        help="Pilih sumber event.",
    )

    parser.add_argument(
        "--category",
        choices=[
            "seminar",
            "workshop",
            "lomba",
            "webinar",
            "all",
        ],
        default="all",
        help="Filter event berdasarkan kategori.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )

    return parser


def get_events(source: str) -> list[Event]:
    if source == "pnl":
        return PNLScraper().scrape()

    if source == "himatik":
        return HimatikScraper().scrape()

    return [
        *PNLScraper().scrape(),
        *HimatikScraper().scrape(),
    ]


def filter_events(
    events: list[Event],
    category: str,
) -> list[Event]:
    if category == "all":
        return events

    return [
        event
        for event in events
        if event.category.lower() == category.lower()
    ]


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    events = get_events(args.source)
    filtered_events = filter_events(
        events=events,
        category=args.category,
    )

    print(f"=== {APP_NAME} ===")
    print(f"Sumber   : {args.source}")
    print(f"Kategori : {args.category}")

    display_events(filtered_events)


if __name__ == "__main__":
    main()