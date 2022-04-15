from repository import EventRepository
from datetime import datetime
from models import Event


class EventService:
    def __init__(self):
        self._repository = EventRepository()
        self._cache = None

    def get_all(self, **event) -> dict:
        return self._repository.get_all_by_date(**event)

    def get_by_email(self, **event):
        return self._repository.get_all_by_creator(**event)

    def add(self, **event) -> bool:
        if not self._repository.is_overlaps_datetime(**event):
            print("Не пересекается")
            self._repository.insert(**event)
            self._repository.session_commit()
            return True

    def delete(self, uid: str):
        self._repository.delete_by_id(uid=uid)
        self._repository.session_commit()

    def change(self, event: dict):
        pass

    def send_email(self, email: str):
        # TODO перенести в mail сервис
        # отправка уведомления на почту
        pass