import streamlit as st
from core.utils import format_events
from services.exceptions import (EventSpecifiedTimeAlreadyCreated,
                                 IntersectionEventsError)

from view.base import BaseView


class ChangeView(BaseView):
    def change_form(self, events):
        placeholder = st.empty()

        self.main_widget()
        start, end = self._get_start_end_date()

        col1, _ = st.columns([4, 7])
        with col1:
            selected_event = st.selectbox(
                "Выберите событие для изменения",
                events,
                format_func=lambda x: format_events(x),
            )
        self.button_widget(7)

        submit = st.button("Изменить событие")

        if submit:
            with st.spinner("Please wait..."):
                try:
                    self._event.change(
                        email=st.session_state.email,
                        instance=selected_event,
                        start_date=start,
                        end_date=end,
                        creator=st.session_state.email,
                        room=st.session_state.room,
                        place=str(st.session_state.place),
                    )
                    placeholder.success("На указанный email отправлено письмо для подтверждения изменения бронирования")

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
            st.warning(
                "События не найдены, попробуйте ввести корректный email или добавить события на вкладке 'Создать'"
            )
