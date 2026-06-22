from collections.abc import Iterable

from .models import Event


def display_events(events: Iterable[Event]) -> None:
    event_list = list(events)

    if not event_list:
        print("\nTidak ada event yang ditemukan.")
        return

    print("\n=== Daftar Event ===")

    for number, event in enumerate(event_list, start=1):
        print(f"\n[{number}] {event.title}")
        print(f"    Kategori : {event.category.title()}")
        print(f"    Tanggal  : {event.date}")
        print(f"    Sumber   : {event.source.upper()}")
        print(f"    Link     : {event.url}")

    print(f"\nTotal event: {len(event_list)}")