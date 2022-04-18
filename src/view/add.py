import streamlit as st
from core.config import *

from view.base import BaseView


class AddEvent(BaseView):
    def add_form(self):
        with st.form("Add_form"):
            start, end = self.combine_datetime()
            st.markdown(
                f"""
                ##### **Данные бронирования**
                ```python
                Комната: {st.session_state.room} Место: {st.session_state.selected}
                {start.strftime("%d.%m.%Y %H:%M")} - Начальная дата и время
                {end.strftime("%d.%m.%Y %H:%M")} - Конечная дата и время
                ```
            """
            )

            submit = st.form_submit_button("Забронировать")

            if submit:
                if self._event.add(
                    start_date=start,
                    end_date=end,
                    creator=st.session_state.email,
                    room=st.session_state.room,
                    place=str(st.session_state.selected),
                ):
                    st.success("На указанный email отправлено письмо для подтверждения события")
                else:
                    st.error("Рабочее место на указанную дату уже занято")

    def main_add(self):

        self.side_bar()
        self.add_form()

        with st.expander(f"Room {st.session_state.room}", expanded=True):
            st.image(
                self.get_image(st.session_state.room),
            )
