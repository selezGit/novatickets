import streamlit as st
from streamlit_option_menu import option_menu

from . import ChangeEvent, CreateEvent, DeleteEvent, ShowEvents


class ViewApp(
    ShowEvents,
    CreateEvent,
    DeleteEvent,
    ChangeEvent,
):
    def run(self) -> None:
        self.hide_menu()
        self.input_email()
        if not "selected" in st.session_state:
            st.session_state.selected = "1"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        with st.sidebar:
            st.markdown(f"User: {st.session_state.email}")
            selected = option_menu(
                None,
                ["Show", "Create", "Delete", "Change"],
                icons=[
                    "calendar3",
                    "calendar-plus",
                    "calendar-x",
                    "calendar-event",
                ],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
        if selected == "Show":
            self.main_show()
        elif selected == "Create":
            self.main_create()
        elif selected == "Delete":
            self.main_delete()
        elif selected == "Change":
            self.main_change()
