from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION, NUMERIC_VALUE_OUT_OF_RANGE, FOREIGN_KEY_VIOLATION
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.auth.exceptions import deleted_user
from app.database.excaptions import does_not_exist, unique_error, data_error


class DatabaseAPI:
    def __init__(self, session: Session):
        self.session = session
        self.exception = does_not_exist

    def get(self, table, exception=None, **kwargs):
        instance = self.session.query(table).filter_by(
            **kwargs
        ).first()

        if not instance:
            raise exception or self.exception

        return instance

    def get_all(self, table, **kwargs):
        return self.session.query(table).filter_by(
            **kwargs
        ).all()

    def create(self, table, data: dict):
        instance = table(**data)

        self.session.add(instance)
        self._pre_save_check()
        self.session.refresh(instance)

        return instance

    def update(self, table, data: dict, **kwargs):
        instance = self.get(table, **kwargs)

        for field, value in data.items():
            setattr(instance, field, value)

        self._pre_save_check()
        self.session.refresh(instance)

        return instance

    def delete(self, table, **kwargs):
        instance = self.get(table, **kwargs)
        self.session.delete(instance)
        self.session.commit()

    def _pre_save_check(self):
        try:
            self.session.commit()
        except (DataError, IntegrityError) as err:
            if isinstance(err.orig, errors.lookup(UNIQUE_VIOLATION)):
                self.session.rollback()
                raise unique_error
            if isinstance(err.orig, errors.lookup(FOREIGN_KEY_VIOLATION)):
                raise deleted_user
            if isinstance(err.orig, errors.lookup(NUMERIC_VALUE_OUT_OF_RANGE)):
                raise data_error
