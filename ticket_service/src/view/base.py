from datetime import datetime, time, timedelta
from typing import Dict, Optional, Tuple

import streamlit as st
from core.config import ROOMS, STREAMLIT_STYLES, TIME, WHITE_LIST
from core.utils import calculate_index, ceil_dt, set_style_button
from services.event import EventService


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

    def date_widget(
        self,
        max_end_date: Optional[datetime] = None,
    ) -> None:
        today = datetime.now()

        if today.time() > time(23, 0):
            today = today.date() + timedelta(days=1)

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
                max_value=max_end_date,
                value=st.session_state.start_date,
                on_change=self.set_datetime,
                key="end_date",
                disabled=st.session_state.all_day,
            )

        with col2:

            start_index = 0

            if today.date() == st.session_state.end_date:
                start_index = TIME.index(ceil_dt(today, timedelta(minutes=30)))

            start_time = st.selectbox(
                "start time",
                TIME,
                index=start_index,
                key="start_time",
                on_change=self.set_datetime,
                disabled=st.session_state.all_day,
            )

            end_index = TIME.index(start_time) + 1

            st.selectbox(
                "end time",
                TIME[end_index:],
                key="end_time",
                on_change=self.set_datetime,
                disabled=st.session_state.all_day,
                format_func=lambda x: self.format_time(x),
            )

    @staticmethod
    def btn_callback(btn: int) -> None:
        st.session_state.selected = str(btn)

    @staticmethod
    def hide_menu():
        st.markdown(
            STREAMLIT_STYLES,
            unsafe_allow_html=True,
        )

    def get_buttons(self) -> Dict[int, str]:
        start, end = self.combine_datetime()

        full_interval = calculate_index(start, end)

        button_dict = {}

        for place, events in self._event.get_all_buttons(
            start_date=start,
            end_date=end,
            room=st.session_state.room,
        ).items():
            interval = sum(calculate_index(event.start_date, event.end_date) for event in events)

            if interval < full_interval and not st.session_state.all_day:
                button_dict[int(place)] = "gold"
            else:
                button_dict[int(place)] = "red"

        return button_dict

    def button_widget(self) -> None:
        colls = [i for i in st.columns([1, 1, 1])]
        style = ""
        places = ROOMS[st.session_state.room]["places"]
        reserved_places = self.get_buttons()

        for y, col in enumerate(colls):
            with col:
                x = 1
                for i in range((y * (places // 3)) + 1, ((places // 3) * (y + 1)) + 1):
                    st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                    if i in reserved_places:
                        style += set_style_button(reserved_places[i], x=x, y=y + 1)
                    else:
                        style += set_style_button("green", x=x, y=y + 1)

                    x += 1
                if y == 2 and places % 3 != 0:
                    for i in range(((places // 3) * (y + 1)) + 1, places + 1):
                        st.button(f"Place {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                        if i in reserved_places:
                            style += set_style_button(reserved_places[i], x=x, y=y + 1)
                        else:
                            style += set_style_button("green", x=x, y=y + 1)
                        x += 1

        st.markdown(
            f"""<style>
            {style}
        </style>""",
            unsafe_allow_html=True,
        )

    def change_room(self):
        if ROOMS[st.session_state.room]["places"] < int(st.session_state.selected):
            st.session_state.selected = "1"

    def side_bar(self):
        with st.sidebar:
            self.date_widget()
            st.selectbox("Please select room", ROOMS, key="room", on_change=self.change_room)
            self.button_widget()

    def input_email(self):
        placeholder = st.empty()

        email = placeholder.text_input(
            "email",
            placeholder="Введите ваш email",
            autocomplete="email",
        )
        if not email:
            st.stop()

        if email and "@" in email and email.split("@")[1] in WHITE_LIST:
            placeholder.empty()
            st.session_state.email = email.strip()
            return
        else:
            st.warning("Введите пожалуйста корректный email или обратитесь в службу поддержки sa@novardis.com")
            st.stop()
