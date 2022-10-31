import streamlit as st
from core.config import BASE_DIR
from streamlit_option_menu import option_menu

from . import ChangeView, CreateView, DeleteView, FAQView, HelloView


class ViewApp(
    ChangeView,
    CreateView,
    DeleteView,
    FAQView,
    HelloView,
):
    def run(self) -> None:
        st.set_page_config(
            page_title="Booking",
            page_icon=BASE_DIR + "/src/static/favicon.png",
            layout="centered",
            initial_sidebar_state="expanded",
        )
        self.hide_menu()

        default_menu = ["Создать", "Изменить", "Удалить", "FAQ"]
        icons = [
            "calendar-plus",
            "calendar-event",
            "calendar-x",
            "info-square",
        ]
        if not "place" in st.session_state:
            st.session_state.place = "1"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        if not "events" in st.session_state:
            st.session_state.events = []

        if not "email" in st.session_state:
            st.session_state.email = ""

        if not st.session_state.email:
            self._event.auth()
            
            if st.session_state.token:
                userdata = self._event.auth.handler_get_userdata()
                st.session_state.email = userdata["userPrincipalName"]
                st.session_state.username = userdata["displayName"]

        with st.sidebar:
            if st.session_state.email:
                if st.button("Выйти"):
                    self._event.auth.logout()

                text = f"""<p style="font-family:serif; font-size: 21px;color: gray;">
                Пользователь: {st.session_state.username}\n {st.session_state.email}</p>"""
                st.markdown(text, unsafe_allow_html=True)
                st.markdown("---")

                selected = option_menu(
                    "Menu",
                    default_menu,
                    icons=icons,
                    menu_icon="cast",
                    default_index=0,
                    orientation="vertical",
                )

        if not st.session_state.email:
            self.main_hello()
        elif selected == "Создать":
            self.main_create()
        elif selected == "Изменить":
            self.main_change()
        elif selected == "Удалить":
            self.main_delete()
        elif selected == "FAQ":
            self.main_faq()
