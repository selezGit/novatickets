import time
import streamlit as st
from core.utils import format_events
from services.exceptions import EventSpecifiedTimeAlreadyCreated, IntersectionEventsError

from view.base import BaseView


class ChangeView(BaseView):
    def change_form(self, events):
        self.main_widget()

        placeholder = st.empty()
        col1, _ = st.columns([3, 1])
        with col1:
            selected_event = st.selectbox(
                "Выберите событие для изменения",
                events,
                format_func=lambda x: format_events(x),
            )
        self.button_widget()

        submit = st.button("Изменить событие")

        if submit:
            try:
                self._event.change(
                    instance=selected_event,
                    **self.get_selected_event(),
                )
                placeholder.success("✅ Бронирование изменено")
                time.sleep(1)
                st.experimental_rerun()
            except (
                IntersectionEventsError,
                EventSpecifiedTimeAlreadyCreated,
            ) as error:
                placeholder.error(error)

    def main_change(self):
        events = self._event.get_by_email(creator=st.session_state.email)
        if events:
            self.change_form(events)
        else:
            st.warning("⚠️ События не найдены, попробуйте добавить их на вкладке 'Создать'")
