import base64
from datetime import datetime, time, timedelta
from typing import Tuple

import streamlit as st
from core.config import *
from PIL import Image
from services.event_service import EventService
from streamlit_option_menu import option_menu


class BaseView:

    _event = EventService()

    def combine_datetime(self) -> Tuple[datetime, datetime]:
        sdt = st.session_state.start_date
        edt = st.session_state.end_date

        stm = st.session_state.start_time
        etm = st.session_state.end_time

        if not st.session_state.all_day:
            start = datetime.combine(sdt, stm)
            end = datetime.combine(edt, etm)
        else:
            start = datetime.combine(sdt, time(0, 0))
            end = datetime.combine(sdt, time(23, 59))

        return start, end

    def date_widget(self) -> None:
        today = datetime.now()

        def set_datetime():
            start, end = self.combine_datetime()
            if start >= end:
                st.session_state.end_date = (start + timedelta(minutes=30)).date()
                st.session_state.end_time = (start + timedelta(minutes=30)).time()

        def set_checkbox():
            start, _ = self.combine_datetime()
            if st.session_state.all_day:
                st.session_state.start_time = time(0, 0)
                st.session_state.end_date = start
                st.session_state.end_time = time(23, 59)

        st.checkbox("All day", key="all_day", on_change=set_checkbox)
        col1, col2 = st.columns(2)
        with col1:
            st.date_input(
                "start date",
                min_value=today,
                value=today,
                on_change=set_datetime,
                key="start_date",
            )
            st.date_input(
                "end date",
                min_value=st.session_state.start_date,
                value=st.session_state.start_date,
                on_change=set_datetime,
                key="end_date",
                disabled=st.session_state.all_day,
            )

        with col2:
            st.time_input(
                "start time",
                value=time(8, 30),
                on_change=set_datetime,
                key="start_time",
                disabled=st.session_state.all_day,
            )

            st.time_input(
                "end time",
                value=time(9, 0),
                on_change=set_datetime,
                key="end_time",
                disabled=st.session_state.all_day,
            )

    # @st.cache(allow_output_mutation=True)
    # def get_base64(self, bin_file) -> base64:
    #     with open(bin_file, "rb") as f:
    #         data = f.read()
    #     return base64.b64encode(data).decode()

    # def set_bg(self, png_file: str) -> None:
    #     bin_str = self.get_base64(png_file)
    #     page_bg_img = (
    #         """
    #         <style>
    #         .stApp {
    #         background-image: url("data:image/png;base64,%s");
    #         background-size: cover;
    #         }
    #         </style>
    #     """
    #         % bin_str
    #     )
    #     st.markdown(page_bg_img, unsafe_allow_html=True)

    def btn_callback(self, btn: int):
        st.session_state.selected = btn

    def button_widget(self) -> None:
        colls = [i for i in st.columns([5, 5, 5])]
        style = ""
        places = ROOMS[st.session_state.room]["places"]
        for y, col in enumerate(colls):
            with col:
                x = 1
                for i in range((y * (places // 3)) + 1, ((places // 3) * (y + 1)) + 1):
                    st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                    style += self.create_btn("green", x=x, y=y + 1)
                    x += 1
                if y == 2 and places % 3 != 0:
                    for i in range(((places // 3) * (y + 1)) + 1, places + 1):
                        st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                        style += self.create_btn("yellow", x=x, y=y + 1)
                        x += 1

        st.markdown(
            f"""<style>
            {style}
        </style>""",
            unsafe_allow_html=True,
        )

    def create_btn(self, state: str, x: int, y: int) -> str:
        return f"""
        
        div:nth-child(5) > div:nth-child({y}) > div:nth-child(1) > div > div:nth-child({x}) > div > button {{
            border-color: {COLORS[state]};
            border-width: 2px;
            width:6em;
            border-radius: 20px;
            height:2em;
            color:#fffffff;
        }}
        div:nth-child(5) > div:nth-child({y}) > div:nth-child(1) > div > div:nth-child({x}) > div > button:hover {{
            background-color: #ff4c4c;
            border-width: 2px;
            width:6em;
            border-radius: 20px;
            height:2em;
            color:#ffffff;
        }}"""

    @st.cache(allow_output_mutation=True)
    def get_image(self, room: str) -> Image:
        return Image.open(IMG_DIR + f"office-{room}.png")

    def change_room(self):
        st.session_state.selected = 1

    def side_bar(self):
        with st.sidebar:
            self.date_widget()
            st.selectbox("Please select room", ROOMS, key="room", on_change=self.change_room)
            self.button_widget()
