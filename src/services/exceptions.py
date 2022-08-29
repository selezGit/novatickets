class EventSpecifiedTimeAlreadyCreated(Exception):
    """Пользователь уже создал бронирование на указанное время"""

    def __init__(self):
        self.message = "❌ Вы не можете забронировать несколько событий в одно и то же время."
        super().__init__(self.message)


class IntersectionEventsError(Exception):
    """Пересечение событий"""

    def __init__(self):
        self.message = "❌ Рабочее место на указанную дату уже занято."
        super().__init__(self.message)


class IntersectionEventsInListError(Exception):
    """Пересечение событий в списке"""

    def __init__(self):
        self.message = "❌ Невозможно добавить бронирование на это время и место так как оно пересекается с уже добавленными событиями."
        super().__init__(self.message)
