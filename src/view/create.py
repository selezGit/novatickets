import time
import streamlit as st
from core.utils import format_dict_events, to_readable_format
from models import Event
from services.exceptions import EventSpecifiedTimeAlreadyCreated, IntersectionEventsError, IntersectionEventsInListError

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
        self.main_widget(is_create=True)
        placeholder = st.empty()

        if st.session_state.append_button:
            try:
                self.append_events(self.get_selected_event())
            except (
                IntersectionEventsInListError,
                EventSpecifiedTimeAlreadyCreated,
                IntersectionEventsError,
            ) as error:
                placeholder.error(error)
        selected_events = st.multiselect(
            "Список бронирований",
            options=st.session_state.events,
            default=st.session_state.events,
            format_func=lambda x: format_dict_events(x),
            key="selected_events",
        )
        self.button_widget()
        submit = st.button("Забронировать")

        if submit:
            try:
                if selected_events:
                    st.session_state.events = []
                    self._event.create_all(selected_events)
                else:
                    self._event.create(**self.get_selected_event())
                placeholder.success("✅ Рабочее место забронировано")
                time.sleep(1)
                st.experimental_rerun()
            except (
                IntersectionEventsError,
                EventSpecifiedTimeAlreadyCreated,
            ) as error:
                placeholder.error(error)
