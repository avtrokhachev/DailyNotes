from datetime import datetime, timedelta
import dataclasses
import pytest
from database.concepts import daily_notes
from random import randint


DAILY_NOTE1 = daily_notes.DailyNote(
    id=5,
    date=datetime.today(),
    message="some text",
)
DAILY_NOTE2 = daily_notes.DailyNote(
    id=7,
    date=datetime.today() + timedelta(days=1),
    message="another text",
)


class TestGetAll:
    def test_return_empty_list_when_no_records(self):
        result = daily_notes.get_all()

        assert result == []

    def test_correctly_returns_many_records(self):
        daily_notes.insert(DAILY_NOTE1)
        daily_notes.insert(DAILY_NOTE2)

        result = daily_notes.get_all()

        assert result == [DAILY_NOTE1, DAILY_NOTE2]


class TestGetById:
    def test_returns_none_when_no_data(self):
        result = daily_notes.get_by_id(id=randint(0, 10**9))

        assert result is None

    def test_returns_corrent_data(self):
        daily_notes.insert(DAILY_NOTE1)
        daily_notes.insert(DAILY_NOTE2)

        result = daily_notes.get_by_id(id=DAILY_NOTE2.id)

        assert result == DAILY_NOTE2


class TestInsert:
    @pytest.mark.parametrize(
        "expected_daily_notes", [
            [DAILY_NOTE1],
            [DAILY_NOTE1, DAILY_NOTE2],
        ],
    )
    def test_correctly_inserts_objects(self, expected_daily_notes):
        for daily_note in expected_daily_notes:
            daily_notes.insert(daily_note=daily_note)

        result = daily_notes.get_all()

        assert result == expected_daily_notes


class TestDelete:
    def test_correctly_deletes_data(self):
        daily_notes.insert(DAILY_NOTE1)

        daily_notes.delete(id=DAILY_NOTE1.id)

        result = daily_notes.get_all()
        assert result == []


class TestUpdate:
    def test_correctly_updates(self):
        daily_notes.insert(DAILY_NOTE1)

        updated_note = dataclasses.replace(DAILY_NOTE1)
        updated_note.message = "update_text"
        daily_notes.update(daily_note=updated_note)

        result = daily_notes.get_all()
        assert result == [updated_note]
