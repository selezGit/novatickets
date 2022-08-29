from typing import Any, Dict, List

from models import Event
from repository import EventRepository

from services.exceptions import (EventSpecifiedTimeAlreadyCreated,
                                 IntersectionEventsError,
                                 IntersectionEventsInListError)

from .oauth2 import MSOauthService


class EventService:
    def __init__(self):
        self._repository = EventRepository()
        self.auth = MSOauthService()

    def get_all(self, **event: Dict[str, Any]) -> dict:
        """Получает все события из postgres по дате"""
        return self._repository.get_all_by_place(**event)

    def get_all_buttons(self, **event: Dict[str, Any]) -> Dict[int, List[Event]]:
        """Получает все события из postgres по кабинету для кнопок"""

        cleared_dict = {}
        {
            cleared_dict.setdefault(
                item.place,
                [],
            ).append(item)
            for item in self._repository.get_all_by_room(**event)
        }
        return cleared_dict

    def get_by_email(self, **event: Dict[str, Any]):
        """Получает все события из postgres по автору события"""
        return self._repository.get_all_by_creator(**event)

    def _check_added_event(self, **event: Dict[str, Any]) -> None:
        """Проверка добавленных событий"""

        if self._repository.is_overlaps_datetime(**event):
            raise IntersectionEventsError()

        if self._repository.is_overlaps_event_creator(**event):
            raise EventSpecifiedTimeAlreadyCreated()

    def is_intersection_added_events_list(
        self,
        events: List[Dict[str, Any]],
        **event: Dict[str, Any],
    ) -> None:
        """
        Проверяет, нет ли пересечения по времени между добавленными в список событиями
        """
        if not events:
            return

        for item in events:
            if item.get("start_date") < event.get("end_date") and item.get("end_date") > event.get("start_date"):
                raise IntersectionEventsInListError()

    def create(self, **event: Dict[str, Any]):
        """Добавляет в postgres событие"""
        self._check_added_event(**event)

        self._repository.insert(**event)
        self._repository.session_commit()

    def create_all(self, events: List[str]):
        """Добавление в postgres список событий"""
        for event in events:
            self._check_added_event(**event)
            self._repository.insert(**event)

        self._repository.session_commit()

    def change(self, **event: Dict[str, Any]):
        """Изменяет в postgres событие"""

        if self._repository.is_overlaps_excluding_event(**event):
            raise IntersectionEventsError()

        if self._repository.is_overlaps_event_creator_excluding_event(**event):
            raise EventSpecifiedTimeAlreadyCreated()

        instance = self._repository.get_by_id(event.pop("instance").uid)

        self._repository.update(instance, **event)
        self._repository.session_commit()

    def delete(self, events: List[Event]):
        """Удаляет в postgres список событий"""

        self._repository.delete_many_events(events)
        self._repository.session_commit()
