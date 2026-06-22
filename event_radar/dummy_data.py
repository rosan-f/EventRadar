from .models import Event


def get_dummy_events() -> list[Event]:
    return [
        Event(
            title="Seminar Nasional Cybersecurity",
            category="seminar",
            date="30 Juni 2026",
            source="pnl",
            url="https://example.com/seminar-cybersecurity",
        ),
        Event(
            title="Workshop Python untuk Pemula",
            category="workshop",
            date="5 Juli 2026",
            source="himatik",
            url="https://example.com/workshop-python",
        ),
        Event(
            title="Lomba UI/UX Mahasiswa",
            category="lomba",
            date="12 Juli 2026",
            source="pnl",
            url="https://example.com/lomba-ui-ux",
        ),
        Event(
            title="Webinar Karier di Bidang Teknologi",
            category="webinar",
            date="18 Juli 2026",
            source="himatik",
            url="https://example.com/webinar-karier",
        ),
    ]