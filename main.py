import argparse


APP_NAME = "EventRadar"
APP_VERSION = "0.1.0"


def create_parser() -> argparse.ArgumentParser:
    """
    Membuat konfigurasi argument untuk CLI EventRadar.
    """

    parser = argparse.ArgumentParser(
        prog="event-radar",
        description=(
            "CLI tool untuk mengambil dan menampilkan "
            "informasi seminar, workshop, lomba, dan webinar."
        ),
    )

    parser.add_argument(
        "--source",
        choices=["pnl", "all"],
        default="all",
        help="Pilih sumber event yang ingin diambil.",
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


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    print(f"=== {APP_NAME} ===")
    print(f"Sumber   : {args.source}")
    print(f"Kategori : {args.category}")


if __name__ == "__main__":
    main()