from typing import Any, List
from uuid import UUID, uuid4

from core.config import *
from db.redis import redis_handler
from models import Event
from repository import EventRepository
from repository.redis import RedisCache

from .mail import MailService


class EventService:
    def __init__(self):
        self._repository = EventRepository()
        self._mail = MailService()
        self._cache = RedisCache(redis_handler)

    def get_all(self, **event) -> dict:
        return self._repository.get_all_by_date(**event)

    def get_all_buttons(self, **event):
        return self._repository.get_all_by_room(**event)

    def get_by_email(self, **event):
        return self._repository.get_all_by_creator(**event)

    def create(self, email: str, **event) -> bool:
        operation = "create"
        if not self._repository.is_overlaps_datetime(**event):
            instance = self._repository.model(**event)
            key = self._put_in_cache(instance, operation)
            self._send(email, key, operation)
            return True

    def delete(self, email: str, events: List[Event]):
        operation = "delete"
        key = self._put_in_cache(events, operation)
        self._send(email, key, operation)

    def change(self, email: str, instance: Event, **event) -> bool:
        operation = "change"
        if not self._repository.is_overlaps_excluding_event(instance.uid, **event):
            instance = self._repository.update(instance, **event)
            key = self._put_in_cache(instance, operation)
            self._send(email, key, operation)
            return True

    def do_task(self, operation, data):
        if operation == "create":
            return self._crate(**data)
        elif operation == "change":
            return self._change(**data)
        elif operation == "delete":
            return self._delete(data)
        else:
            return False

    def _crate(self, **event):
        if not self._repository.is_overlaps_datetime(**event):
            self._repository.insert(**event)
            self._repository.session_commit()
            return True

    def _change(self, **event):
        if not self._repository.is_overlaps_excluding_event(**event):
            instance = self._repository.get_by_id(event.get("uid"))
            self._repository.update(instance, **event) is not None
            self._repository.session_commit()
            return True

    def _delete(self, events: List[Event]):
        self._repository.delete_many_events(events)
        self._repository.session_commit()
        return True

    def _put_in_cache(self, instance: Any, operation: str) -> UUID:
        key = uuid4()
        if isinstance(instance, list):
            self._cache.put_list(f"{key}::{operation}", instance)
        else:
            self._cache.put(f"{key}::{operation}", instance)
        return key

    def _send(self, email: str, key: UUID, operation: str) -> None:
        self._mail.send_email(
            email,
            CACHE_URL + str(key),
            OPERATIONS[operation],
        )
