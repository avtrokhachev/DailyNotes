import typing as tp

import sqlalchemy
import secrets


class Repository:
    _engine: tp.Optional[sqlalchemy.Engine] = None

    def __new__(cls, *args, **kwargs) -> sqlalchemy.Engine:
        if not cls._engine:
            print(1)
            cls._engine = sqlalchemy.create_engine(**secrets.get_database_connection())

        return cls._engine

    @classmethod
    def run(cls, *args, **kwargs) -> sqlalchemy.CursorResult:
        with cls._engine.begin() as conn:
            result = conn.execute(*args, **kwargs)

        return result

    @classmethod
    def get_engine(cls, *args, **kwargs) -> tp.Optional[sqlalchemy.Engine]:
        return cls._engine

    @classmethod
    def disable_engine(self, *args, **kwargs) -> None:
        print(2)
        if self._engine:
            self._engine.dispose()
        self._engine = None
