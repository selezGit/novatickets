import streamlit as st
from core.config import ROOMS
from core.utils import to_readable_format
from models import Event
from services.exceptions import (EventSpecifiedTimeAlreadyCreated,
                                 IntersectionEventsError)

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
        self.date_widget()
        start, end = self._get_start_end_date()

        st.selectbox("Выберите комнату", ROOMS, key="room", on_change=self.set_room)
        col1, col2 = st.columns([1, 2])
        with col1:
            self.booking(start, end)
        with col2:
            self.status(start, end)
        self.button_widget()

        _, col2, col3 = st.columns(3)
        with col2:
            submit = st.button("Забронировать")

        with col3:
            if submit:
                with st.spinner("Please wait..."):
                    try:
                        self._event.create(
                            email=st.session_state.email,
                            start_date=start,
                            end_date=end,
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
