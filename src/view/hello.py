import streamlit as st
from core.config.base import BASE_DIR

from view.base import BaseView


class HelloView(BaseView):
    def main_hello(self):

        _, col, _ = st.columns([2, 2, 1])
        with col:
            st.image(BASE_DIR + "/src/static/novalogo.png", width=100)

        hello_text = f'<p style="font-size: 20px;text-align: center;">Добро пожаловать на страницу бронирования рабочих мест в офисе компании Novardis.</p>'
        st.markdown(hello_text, unsafe_allow_html=True)

        if not st.session_state.is_authorized:
            _, col, _ = st.columns([2, 2, 1])
            with col:
                st.button("Войти", on_click=self._event.auth.login)

        _, col, _ = st.columns([1, 6, 1])
        with col:
            st.caption("Для входа в систему авторизуйтесь под своей рабочей учётной записью.")
