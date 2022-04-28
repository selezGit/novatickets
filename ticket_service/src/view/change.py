import streamlit as st
from core.config import ROOMS
from core.utils import format_events
from services.exceptions import EventSpecifiedTimeAlreadyCreated, IntersectionEventsError

from view.base import BaseView


class ChangeView(BaseView):
    def change_form(self, events):
        placeholder = st.empty()
        self.date_widget()
        start, end = self._get_start_end_date()

        col1, col2 = st.columns([1, 2])
        with col1:
            st.selectbox("Выберите комнату", ROOMS, key="room", on_change=self.set_room)

        with col2:
            selected_event = st.selectbox(
                "Выберите событие для изменения",
                events,
                format_func=lambda x: format_events(x),
            )
            
        col1, col2 = st.columns([1, 2])
        with col1:
            self.booking(start, end)
        with col2:
            self.status(start, end)
        
        self.button_widget()

        _, col2, col3 = st.columns(3)
        with col2:
            submit = st.button("Изменить событие")

        with col3:
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
                        placeholder.success(
                            "На указанный email отправлено письмо для подтверждения изменения бронирования"
                        )
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
            st.warning("События не найдены, попробуйте ввести корректный email или добавить события на вкладке Add")
