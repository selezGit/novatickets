from signal import raise_signal
from typing import Any, Dict, List
from uuid import UUID, uuid4

from core.config import CACHE_URL, OPERATIONS
from db.redis import redis_handler
from models import Event
from repository import EventRepository
from repository.redis import RedisCache

from services.exceptions import (EventSpecifiedTimeAlreadyCreated,
                                 IntersectionEventsError,
                                 IntersectionEventsInListError)

from .mail import MailService


class EventService:
    def __init__(self):
        self._repository = EventRepository()
        self._mail = MailService()
        self._cache = RedisCache(redis_handler)

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

    def create_all(self, events: List[Dict[str, Any]]) -> None:
        """Добавляет несколько событий в redis необходимые проверки
        были произведены на этапе добавления событий в список"""

        operation = "create_all"
        instances_list = [Event(**event) for event in events]

        key = self._put_in_cache(instances_list, operation)
        self._send(instances_list[0].creator, key, operation, events)

    def create(self, **event: Dict[str, Any]) -> None:
        """Добавляет в redis событие на добавление"""

        self._check_added_event(**event)

        operation = "create"
        instance = self._repository.model(**event)
        key = self._put_in_cache(instance, operation)
        self._send(event.get("creator"), key, operation, [event])

    def _check_added_event(self, **event: Dict[str, Any]) -> None:

        if self._repository.is_overlaps_datetime(**event):
            raise IntersectionEventsError()

        if self._repository.is_overlaps_event_creator(**event):
            raise EventSpecifiedTimeAlreadyCreated()

    def delete(self, events: List[Event]):
        """Добавляет в redis событие на удаление"""

        operation = "delete"
        key = self._put_in_cache(events, operation)

        self._send(events[0].creator, key, operation, events)

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

    def change(self, instance: Event, **event: Dict[str, Any]) -> bool:
        """Добавляет в redis событие на изменение"""

        if self._repository.is_overlaps_excluding_event(**event):
            raise IntersectionEventsError()

        operation = "change"
        instance = self._repository.update(instance, **event)

        if self._repository.is_overlaps_event_creator_excluding_event(**instance.to_dict()):
            raise EventSpecifiedTimeAlreadyCreated()

        key = self._put_in_cache(instance, operation)
        self._send(event.get("creator"), key, operation, [instance])

    def do_task(self, operation, data):
        """Функция для обработки ветвления"""

        if operation == "create":
            return self._crate(**data)
        elif operation == "create_all":
            return self._create_all(data)
        elif operation == "change":
            return self._change(**data)
        elif operation == "delete":
            return self._delete(data)

    def _crate(self, **event: Dict[str, Any]):
        """Добавляет в postgres событие"""
        self._check_added_event(**event)

        self._repository.insert(**event)
        self._repository.session_commit()

    def _create_all(self, events: List[str]):
        for event in events:
            self._check_added_event(**event)
            self._repository.insert(**event)

        self._repository.session_commit()

    def _change(self, **event: Dict[str, Any]):
        """Изменяет в postgres событие"""

        if self._repository.is_overlaps_excluding_event(**event):
            raise IntersectionEventsError()

        if self._repository.is_overlaps_event_creator_excluding_event(**event):
            raise EventSpecifiedTimeAlreadyCreated()

        instance = self._repository.get_by_id(event.get("uid"))
        self._repository.update(instance, **event)
        self._repository.session_commit()

    def _delete(self, events: List[Event]):
        """Удаляет в postgres список событий"""

        self._repository.delete_many_events(events)
        self._repository.session_commit()

    def _put_in_cache(self, instance: Any, operation: str) -> UUID:
        key = uuid4()
        if isinstance(instance, list):
            self._cache.put_list(f"{key}::{operation}", instance)
        else:
            self._cache.put(f"{key}::{operation}", instance)
        return key

    def _send(self, email: str, key: UUID, operation: str, data: List[Dict[str, str]]) -> None:
        self._mail.send_email(
            email,
            CACHE_URL + str(key),
            OPERATIONS[operation],
            data,
        )
