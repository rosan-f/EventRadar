import argparse

from event_radar.formatter import display_events
from event_radar.models import Event
from event_radar.scrapers.factory import ScraperFactory


APP_NAME = "EventRadar"
APP_VERSION = "0.6.0"


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
        choices=["pnl", "dicoding", "all"],
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
        "--search",
        type=str,
        default=None,
        help="Cari event berdasarkan judul.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )

    return parser


def get_events(source: str) -> list[Event]:
    if source == "all":
        events: list[Event] = []

        for scraper in ScraperFactory.create_all():
            events.extend(scraper.scrape())

        return events

    scraper = ScraperFactory.create(source)

    return scraper.scrape()


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


def search_events(
    events: list[Event],
    keyword: str | None,
) -> list[Event]:
    if not keyword:
        return events

    normalized_keyword = keyword.lower()

    return [
        event
        for event in events
        if normalized_keyword in event.title.lower()
    ]


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    try:
        events = get_events(args.source)

        filtered_events = filter_events(
            events=events,
            category=args.category,
        )

        searched_events = search_events(
            events=filtered_events,
            keyword=args.search,
        )

        print(f"=== {APP_NAME} ===")
        print(f"Sumber   : {args.source}")
        print(f"Kategori : {args.category}")

        if args.search:
            print(f"Pencarian: {args.search}")

        display_events(searched_events)

    except (ValueError, RuntimeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()