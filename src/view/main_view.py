import streamlit as st
from core.config import BASE_DIR
from streamlit_option_menu import option_menu

from . import ChangeView, CreateView, DeleteView, FAQView


class ViewApp(
    ChangeView,
    CreateView,
    DeleteView,
    FAQView,
):
    def run(self) -> None:
        st.set_page_config(
            page_title="Booking",
            page_icon=BASE_DIR + "/src/static/favicon.png",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self.hide_menu()
        self.input_email()

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

        with st.sidebar:
            st.markdown(f"### {st.session_state.email}")
            selected = option_menu(
                None,
                default_menu,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
        if selected == "Создать":
            self.main_create()
        elif selected == "Изменить":
            self.main_change()
        elif selected == "Удалить":
            self.main_delete()
        elif selected == "FAQ":
            self.main_faq()
