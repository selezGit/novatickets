import streamlit as st
from core.config import *
from streamlit_option_menu import option_menu

from view.add import AddEvent
from view.show import ShowEvents


class ViewApp(
    ShowEvents,
    AddEvent,
):
    def run(self) -> None:
        # self.set_bg(f"img/LogoNovardisNew.png")
        if not "selected" in st.session_state:
            st.session_state.selected = 1

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
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"background-color": "#fafafa"},
                    "icon": {"color": "black", "font-size": "15px"},
                    # "nav-link": {"font-size": "15px", "margin": "0px", "--hover-color": "#eee"},
                },
            )
        if selected == "Show":
            self.show_events()
        elif selected == "Add":
            self.add_event()
        elif selected == "Delete":
            pass
        elif selected == "Change":
            pass
