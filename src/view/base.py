from datetime import datetime, time, timedelta
from typing import Tuple

import streamlit as st
from core.config import *
from PIL import Image
from services.event_service import EventService


class BaseView:

    _event = EventService()

    def combine_datetime(self) -> Tuple[datetime, datetime]:
        sdt = st.session_state.start_date
        edt = st.session_state.end_date

        stm = datetime.strptime(st.session_state.start_time, "%H:%M").time()
        etm = datetime.strptime(st.session_state.end_time, "%H:%M").time()

        if not st.session_state.all_day:
            start = datetime.combine(sdt, stm)
            end = datetime.combine(edt, etm)
        else:
            start = datetime.combine(sdt, time(0, 0))
            end = datetime.combine(sdt + timedelta(days=1), time(0, 0))
        return start, end

    def format_time(self, end_time):
        if st.session_state.start_date != st.session_state.end_date or st.session_state.all_day:
            return end_time

        start = datetime.strptime(st.session_state.start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        delta = (end - start).total_seconds()
        duration = delta // 60 / 60
        if duration % 1 == 0:
            duration = int(duration)

        return f"{end_time} ({duration} hours)"

    def set_datetime(self):
        start, end = self.combine_datetime()

        if start >= end:
            st.session_state.end_date = (start + timedelta(minutes=30)).date()
            st.session_state.end_time = (start + timedelta(minutes=30)).strftime("%H:%M")

    def date_widget(self) -> None:
        today = datetime.now()

        st.checkbox("All day", key="all_day")
        col1, col2 = st.columns([2, 3])
        with col1:
            st.date_input(
                "start date",
                min_value=today,
                value=today,
                on_change=self.set_datetime,
                key="start_date",
            )
            st.date_input(
                "end date",
                min_value=st.session_state.start_date,
                value=st.session_state.start_date,
                on_change=self.set_datetime,
                key="end_date",
                disabled=st.session_state.all_day,
            )

        with col2:
            st.selectbox(
                "start time",
                TIME,
                index=18,
                key="start_time",
                on_change=self.set_datetime,
                disabled=st.session_state.all_day,
            )

            index = 0
            if st.session_state.start_date == st.session_state.end_date:
                index = TIME.index(st.session_state.start_time)

            st.selectbox(
                "end time",
                TIME[index + 1 :],
                key="end_time",
                on_change=self.set_datetime,
                disabled=st.session_state.all_day,
                format_func=lambda x: self.format_time(x),
            )

    def to_readable_format(self, date: datetime) -> str:
        return date.strftime(r"%d %b %Y %H:%M")

    def btn_callback(self, btn: int) -> None:
        st.session_state.selected = str(btn)

    def get_buttons(self):
        start, end = self.combine_datetime()
        return self._event.get_all_buttons(
            start_date=start,
            end_date=end,
            room=st.session_state.room,
        )

    def button_widget(self) -> None:
        colls = [i for i in st.columns([5, 5, 5])]
        style = ""
        places = ROOMS[st.session_state.room]["places"]

        reserved_places = [int(event.place) for event in self.get_buttons()]

        for y, col in enumerate(colls):
            with col:
                x = 1
                for i in range((y * (places // 3)) + 1, ((places // 3) * (y + 1)) + 1):
                    st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                    if i in reserved_places:
                        style += self.create_btn("red", x=x, y=y + 1)
                    else:
                        style += self.create_btn("green", x=x, y=y + 1)

                    x += 1
                if y == 2 and places % 3 != 0:
                    for i in range(((places // 3) * (y + 1)) + 1, places + 1):
                        st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                        if i in reserved_places:
                            style += self.create_btn("red", x=x, y=y + 1)
                        else:
                            style += self.create_btn("green", x=x, y=y + 1)
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
        if ROOMS[st.session_state.room]["places"] < int(st.session_state.selected):
            st.session_state.selected = "1"

    def side_bar(self):
        with st.sidebar:
            self.date_widget()
            st.selectbox("Please select room", ROOMS, key="room", on_change=self.change_room)
            self.button_widget()

    def input_email(self):
        # TODO тут надо сделать проверку на наличие в списке разрешённых
        placeholder = st.empty()

        email = placeholder.text_input(
            "email",
            value="selezard",
            placeholder="Введите ваш email",
            key="email",
            autocomplete="email",
        )
        if not email:
            st.stop()

        if email:
            placeholder.empty()

    def format_events(self, event):
        return f"{self.to_readable_format(event.start_date)} — {self.to_readable_format(event.end_date)} Комната: {event.room} место: {event.place}"
