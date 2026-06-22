from dataclasses import dataclass


@dataclass
class Event:
    title: str
    category: str
    date: str
    source: str
    url: str