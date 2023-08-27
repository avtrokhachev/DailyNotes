import typing as tp
from .models import DailyNote
from .table import DailyNotes
from database.concepts import database
import sqlalchemy


def get_all() -> list[DailyNote]:
    query = sqlalchemy.select(DailyNotes)
    result = database.Repository.run(query).fetchall()

    return [DailyNote(*daily_note) for daily_note in result]


def get_by_id(id: int) -> tp.Optional[DailyNote]:
    query = sqlalchemy.select(DailyNotes).where(DailyNotes.id == id)
    result = database.Repository.run(query).fetchone()

    if result is not None:
        result = DailyNote(*result)
    return result


def insert(daily_note: DailyNote) -> None:
    query = sqlalchemy.insert(DailyNotes).values(daily_note.to_primitive())
    database.Repository.run(query)


def delete(id: int) -> None:
    query = sqlalchemy.delete(DailyNotes).where(DailyNotes.id == id)
    database.Repository.run(query)


def update(daily_note: DailyNote) -> None:
    query = sqlalchemy.update(DailyNotes).values(daily_note.to_primitive())
    database.Repository.run(query)