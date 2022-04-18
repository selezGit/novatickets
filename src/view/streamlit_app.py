import streamlit as st
from core.config import *
from streamlit_option_menu import option_menu

from . import AddEvent, ChangeEvent, DeleteEvent, ShowEvents


class ViewApp(
    ShowEvents,
    AddEvent,
    DeleteEvent,
    ChangeEvent,
):
    def run(self) -> None:
        self.input_email()

        if not "selected" in st.session_state:
            st.session_state.selected = "1"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        with st.sidebar:
            selected = option_menu(
                st.session_state.email,
                ["Show", "Add", "Delete", "Change"],
                icons=[
                    "calendar3",
                    "calendar-plus",
                    "calendar-x",
                    "calendar-event",
                ],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"background-color": "#fafafa"},
                    "icon": {"color": "black", "font-size": "15px"},
                },
            )
        if selected == "Show":
            self.main_show()
        elif selected == "Add":
            self.main_add()
        elif selected == "Delete":
            self.main_delete()
        elif selected == "Change":
            self.main_change()
