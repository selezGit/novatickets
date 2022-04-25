import streamlit as st

from view.base import BaseView
from core.config import ROOMS


class CreateEvent(BaseView):
    def create_form(self):
        self.date_widget()
        start, end = self.combine_datetime()

        col1, col2 = st.columns([1, 2])
        with col1:
            st.selectbox("Please select room", ROOMS, key="room", on_change=self.change_room)
        with col2:
            st.markdown(
                f"""
                ###### Данные бронирования
                ```python
                Комната: {st.session_state.room} Место: {st.session_state.selected}
                {start.strftime("%d.%m.%Y %H:%M")} - Начальная дата и время
                {end.strftime("%d.%m.%Y %H:%M")} - Конечная дата и время
                ```
            """
            )
        self.button_widget()

        _, col2, _ = st.columns(3)
        with col2:
            submit = st.button("Забронировать")

        if submit:
            with st.spinner("Please wait..."):
                if self._event.create(
                    email=st.session_state.email,
                    start_date=start,
                    end_date=end,
                    creator=st.session_state.email,
                    room=st.session_state.room,
                    place=str(st.session_state.selected),
                ):
                    st.success("На указанный email отправлено письмо для подтверждения бронирования")
                else:
                    st.error("Рабочее место на указанную дату уже занято")

    def main_create(self):
        self.create_form()

        with st.expander(f"Room {st.session_state.room}", expanded=False):
            st.image(
                self.get_image(st.session_state.room),
            )
