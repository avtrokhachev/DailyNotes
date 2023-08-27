from datetime import datetime

from dataclasses import dataclass


@dataclass
class DailyNote:
    id: int
    date: datetime
    message: str

    def to_primitive(self) -> dict:
        return self.__dict__
