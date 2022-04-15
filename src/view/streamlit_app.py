import streamlit as st
from core.config import *
from streamlit_option_menu import option_menu

from view.add import AddEvent
from view.show import ShowEvents
from view.delete import DeleteEvent


class ViewApp(
    ShowEvents,
    AddEvent,
    DeleteEvent,
):
    def run(self) -> None:
        # self.set_bg(f"img/LogoNovardisNew.png")
        if not "selected" in st.session_state:
            st.session_state.selected = "1"

        if not "email" in st.session_state:
            st.session_state.email = "-"

        if not "all_day" in st.session_state:
            st.session_state.all_day = False

        with st.sidebar:
            selected = option_menu(
                "Menu",
                ["Show", "Add", "Delete", "Change"],
                icons=[
                    "calendar3",
                    "calendar-plus",
                    "calendar-x",
                    "calendar-event",
                ],
                menu_icon="cast",
                default_index=2,
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
            pass
        elif selected == "Change":
            pass
