from sqlalchemy import Column, Integer, Text, DateTime

from database.concepts import database


class DailyNotes(database.Base):
    __tablename__ = "daily_notes"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    message = Column(Text)
