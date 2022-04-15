import streamlit as st
from core.config import *

from view.base import BaseView


class AddEvent(BaseView):
    def add_form(self):
        with st.form("Add_form"):
            start, end = self.combine_datetime()
            st.markdown(
                f"""
                ```python
                Комната: {st.session_state.room}
                Выбранное место: {st.session_state.selected}
                Начальная дата: {start}
                Конечная дата: {end}
                Email: {st.session_state.email}
                ```
            """
            )
            email = st.text_input(
                "email",
                placeholder="Введите ваш email для подтверждения бронирования",
                key="email",
                autocomplete="email",
            )

            submit = st.form_submit_button("Submit")

            if submit:
                if not email:
                    st.warning("Введите пожалуйста корректный e-mail")
                else:
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
