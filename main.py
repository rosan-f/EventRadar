import argparse

from event_radar.dummy_data import get_dummy_events
from event_radar.formatter import display_events
from event_radar.models import Event


APP_NAME = "EventRadar"
APP_VERSION = "0.1.0"


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
        help="Pilih sumber event yang ingin ditampilkan.",
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


def filter_events(
    events: list[Event],
    source: str,
    category: str,
) -> list[Event]:
    filtered_events = events

    if source != "all":
        filtered_events = [
            event
            for event in filtered_events
            if event.source.lower() == source.lower()
        ]

    if category != "all":
        filtered_events = [
            event
            for event in filtered_events
            if event.category.lower() == category.lower()
        ]

    return filtered_events


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    events = get_dummy_events()

    filtered_events = filter_events(
        events=events,
        source=args.source,
        category=args.category,
    )

    print(f"=== {APP_NAME} ===")
    print(f"Sumber   : {args.source}")
    print(f"Kategori : {args.category}")

    display_events(filtered_events)


if __name__ == "__main__":
    main()