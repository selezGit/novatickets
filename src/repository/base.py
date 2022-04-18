from typing import TypeVar, Type

from db.postgres import Base, get_db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import Select

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    model: Type[ModelType] = None

    def __init__(self):
        self.session = next(get_db())

    def get_by_id(self, uid: str):
        return self._get_one_by_query(self.session.query(self.model).filter(self._get_model_id_field() == uid))

    def delete_by_id(self, uid: str):
        self.session.query(self.model).filter(self._get_model_id_field() == uid).delete()

    def session_commit(self):
        try:
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise err

    def exists(self, **filters) -> bool:
        return self.session.query(self._get_model_id_field()).filter_by(**filters).first() is not None

    def insert(self, **data) -> Type[ModelType]:
        instance = self.model(**data)
        self.session.add(instance)
        return instance

    def update(self, instance, **data) -> Type[ModelType]:
        self.session.query(self.model).filter(self.model.uid == instance.uid).update(data)
        return instance

    def get(self, **filters):
        return self.session.query(self.model).filter_by(**filters).one()

    def all(self, **filters):
        return self.session.query(self.model).filter_by(**filters).all()

    def _get_model_id_field(self):
        id_field = getattr(self.model, "uid", None)

        if id_field is None:
            raise ValueError("Use model with `uid` field")
        return id_field

    def _get_all_by_query(self, query: Select):
        try:
            return query.all()
        except NoResultFound:
            return None

    def _get_one_by_query(self, query: Select):
        try:
            return query.one()
        except NoResultFound:
            return None
