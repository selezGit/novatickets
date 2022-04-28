class EventSpecifiedTimeAlreadyCreated(Exception):
    """Пользователь уже создал бронирование на указанное время"""

    def __init__(self):
        self.message = "Вы не можете забронировать несколько событий в одно и то же время."
        super().__init__(self.message)


class IntersectionEventsError(Exception):
    """Пересечение событий"""

    def __init__(self):
        self.message = "Рабочее место на указанную дату уже занято."
        super().__init__(self.message)
