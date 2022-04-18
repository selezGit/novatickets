from operator import ge
from models.event import Event
from sqlalchemy import and_

from repository.base import BaseRepository


class EventRepository(BaseRepository):
    model = Event

    def get_all_by_date(self, **event):
        # ограничить только одним раб. местом
        return self._get_all_by_query(
            self._occurrence_query(**event)
            .filter(
                self.model.room == event.get("room"),
                self.model.place == event.get("place"),
            )
            .order_by(self.model.start_date)
        )

    def get_all_by_room(self, **event):
        return self._get_all_by_query(
            self._occurrence_query(**event).filter(
                self.model.room == event.get("room"),
            )
        )

    def is_overlaps_datetime(self, **event) -> bool:
        return self._get_one_by_query(self._overlaps_query(**event)) is not None

    def is_overlaps_excluding_event(self, uid: str, **event):
        return self._get_one_by_query(self._overlaps_query(**event).where(self.model.uid != uid)) is not None

    def _overlaps_query(self, **event):
        # TODO необходимо добавить ещё два ключа is_cancelled, is_verified
        return self.session.query(self.model).filter(
            and_(
                self.model.start_date <= event.get("end_date"),
                self.model.end_date >= event.get("start_date"),
                self.model.room == event.get("room"),
                self.model.place == event.get("place"),
            )
        )

    def _occurrence_query(self, **event):
        return self.session.query(self.model).filter(
            self.model.start_date <= event.get("end_date"),
            self.model.end_date >= event.get("start_date"),
        )

    def get_all_by_creator(self, **event):
        return self._get_all_by_query(
            self.session.query(self.model)
            .filter(
                self.model.creator == event.get("creator"),
            )
            .order_by(self.model.start_date)
        )
