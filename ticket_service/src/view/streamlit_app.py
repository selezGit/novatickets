import streamlit as st
from core.config import MANAGERS
from streamlit_option_menu import option_menu

from . import (
    ChangeView,
    CreateView,
    DeleteView,
    FAQView,
    ManagerView,
)


class ViewApp(
    ChangeView,
    CreateView,
    DeleteView,
    ManagerView,
    FAQView,
):
    def run(self) -> None:
        self.hide_menu()
        self.input_email()

        default_menu = ["Создать", "Изменить", "Удалить", "FAQ"]
        icons = [
            "calendar-plus",
            "calendar-event",
            "calendar-x",
            "info-square",
        ]

        if st.session_state.email in MANAGERS:
            default_menu.append("Manager")
            icons.append("lock")

        if not "place" in st.session_state:
            st.session_state.place = "1"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        with st.sidebar:
            st.markdown(f"### Пользователь: {st.session_state.email}")
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
        elif selected == "Manager":
            self.main_manager()
        elif selected == "FAQ":
            self.main_faq()
