from models.event import Event
from sqlalchemy import and_

from repository.base import BaseRepository
from typing import List


class EventRepository(BaseRepository):
    model = Event

    def get_all_by_date(self, start, end):
        return self._get_all_by_query(
            self.session.query(self.model)
            .filter(
                self.model.start_date >= start,
                self.model.end_date <= end,
            )
            .order_by(self.model.start_date)
        )

    def get_all_by_place(self):
        pass

    def is_overlaps_datetime(self, **event) -> bool:
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    self.model.start_date <= event.get("end_date"),
                    self.model.end_date >= event.get("start_date"),
                    self.model.room == event.get("room"),
                    self.model.place == event.get("place"),
                )
            )
            .first()
        ) is not None
