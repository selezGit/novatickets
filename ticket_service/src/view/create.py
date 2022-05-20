import streamlit as st
from core.utils import to_readable_format
from models import Event
from services.exceptions import EventSpecifiedTimeAlreadyCreated, IntersectionEventsError

from view.base import BaseView


class CreateView(BaseView):
    @st.cache
    def conversion_item(self, item: Event) -> str:
        return f"""
        Комната: {item.room} Место: {item.place}
        Забронировал: {item.creator}
        {to_readable_format(item.start_date)} - Начальная дата и время
        {to_readable_format(item.end_date)} - Конечная дата и время
         """

    def main_create(self):
        placeholder = st.empty()
        self.main_widget()
        self.button_widget(6)
        submit = st.button("Забронировать")

        if submit:
            with st.spinner("Please wait..."):
                try:
                    self._event.create(
                        email=st.session_state.email,
                        start_date=st.session_state.start_datetime,
                        end_date=st.session_state.end_datetime,
                        creator=st.session_state.email,
                        room=st.session_state.room,
                        place=str(st.session_state.place),
                    )
                    placeholder.success("На указанный email отправлено письмо для подтверждения бронирования")
                except (
                    IntersectionEventsError,
                    EventSpecifiedTimeAlreadyCreated,
                ) as error:
                    placeholder.error(error)
