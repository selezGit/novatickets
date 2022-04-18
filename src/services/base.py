from abc import ABC, abstractmethod


class EmailNotification(ABC):
    @abstractmethod
    def send_notify(self, data_to_send: dict):
        pass
