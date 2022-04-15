from datetime import datetime
from models.event import Event
from sqlalchemy import and_

from repository.base import BaseRepository
from typing import List


class EventRepository(BaseRepository):
    model = Event

    def get_all_by_date(self, **event):
        # ограничить только одним раб. местом
        return self._get_all_by_query(
            self.session.query(self.model)
            .filter(
                self.model.start_date <= event.get("end_date"),
                self.model.end_date >= event.get("start_date"),
                self.model.room == event.get("room"),
                self.model.place == event.get("place"),
            )
            .order_by(self.model.start_date)
        )

    def is_overlaps_datetime(self, **event) -> bool:
        return (
            self._get_one_by_query(
                self.session.query(self.model).filter(
                    and_(
                        self.model.start_date <= event.get("end_date"),
                        self.model.end_date >= event.get("start_date"),
                        self.model.room == event.get("room"),
                        self.model.place == event.get("place"),
                    )
                )
            )
            is not None
        )

    def get_all_by_creator(self, **event):
        return self._get_all_by_query(
            self.session.query(self.model)
            .filter(
                self.model.creator == event.get("creator"),
            )
            .order_by(self.model.start_date)
        )
