import streamlit as st
from core.config import MANAGERS
from streamlit_option_menu import option_menu

from . import ChangeView, CreateView, DeleteView, FAQView, ManagerView, ShowView


class ViewApp(
    ChangeView,
    CreateView,
    DeleteView,
    ShowView,
    ManagerView,
    FAQView,
):
    def run(self) -> None:
        self.hide_menu()
        self.input_email()

        default_menu = ["Show", "Create", "Delete", "Change", "FAQ"]
        icons = [
            "calendar3",
            "calendar-plus",
            "calendar-x",
            "calendar-event",
            "info-square",
        ]

        if st.session_state.email in MANAGERS:
            default_menu.append("Manager")
            icons.append("lock")

        if not "selected" in st.session_state:
            st.session_state.selected = "1"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        with st.sidebar:
            st.markdown(f"### User: {st.session_state.email}")
            selected = option_menu(
                None,
                default_menu,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
        if selected == "Show":
            self.main_show()
        elif selected == "Create":
            self.main_create()
        elif selected == "Change":
            self.main_change()
        elif selected == "Delete":
            self.main_delete()
        elif selected == "Manager":
            self.main_manager()
        elif selected == "FAQ":
            self.main_faq()
