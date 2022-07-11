from datetime import datetime, time, timedelta
from typing import Dict

import streamlit as st
from core.config import ROOMS, STREAMLIT_STYLES, TIME, WHITE_LIST
from core.utils import calculate_index, ceil_dt, set_style_button, to_readable_format
from services.event import EventService


class BaseView:
    _event = EventService()

    def _update_start_end_date(self):
        sdt = st.session_state.start_date
        edt = st.session_state.end_date

        stm = datetime.strptime(st.session_state.start_time, "%H:%M").time()
        etm = datetime.strptime(st.session_state.end_time, "%H:%M").time()

        if not st.session_state.all_day:
            st.session_state.start_datetime = datetime.combine(sdt, stm)
            st.session_state.end_datetime = datetime.combine(edt, etm)
        else:
            st.session_state.start_datetime = datetime.combine(sdt, time(0, 0))
            st.session_state.end_datetime = datetime.combine(sdt + timedelta(days=1), time(0, 0))

    def format_time(self, end_time) -> str:
        if st.session_state.start_date != st.session_state.end_date or st.session_state.all_day:
            return end_time

        start = datetime.strptime(st.session_state.start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        delta = (end - start).total_seconds()
        duration = delta // 60 / 60
        if duration % 1 == 0:
            duration = int(duration)

        return f"{end_time} ({duration} hours)"

    def main_widget(
        self,
    ) -> None:
        today = datetime.now()

        if today.time() > time(23, 0):
            today = today + timedelta(days=1)

        st.checkbox("Весь день", key="all_day")

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            st.date_input(
                "Начальная дата",
                min_value=today,
                value=today,
                on_change=self._update_start_end_date,
                key="start_date",
            )

            st.date_input(
                "Конечная дата",
                min_value=st.session_state.start_date,
                max_value=st.session_state.start_date + timedelta(days=3),
                value=st.session_state.start_date,
                on_change=self._update_start_end_date,
                key="end_date",
                disabled=st.session_state.all_day,
            )
            st.selectbox("Выберите комнату", ROOMS, key="room", on_change=self.set_room)

        with col2:
            start_index = 0

            if today.date() <= st.session_state.end_date and not today.time() > time(23, 0):
                start_index = TIME.index(ceil_dt(today, timedelta(minutes=30)))

            start_time = st.selectbox(
                "Начальное время",
                options=TIME[:-1],
                index=start_index,
                key="start_time",
                on_change=self._update_start_end_date,
                disabled=st.session_state.all_day,
            )

            end_index = TIME.index(start_time) + 1

            st.selectbox(
                "Конечное время",
                options=TIME[end_index:],
                key="end_time",
                on_change=self._update_start_end_date,
                disabled=st.session_state.all_day,
                format_func=lambda x: self.format_time(x),
            )
        with col3:
            self.booking()
            self.status()

    @staticmethod
    def btn_callback(btn: int):
        st.session_state.place = str(btn)

    @staticmethod
    def hide_menu():
        st.markdown(
            STREAMLIT_STYLES,
            unsafe_allow_html=True,
        )

    def _get_reserved_places(self) -> Dict[int, str]:
        full_interval = calculate_index(st.session_state.start_datetime, st.session_state.end_datetime)

        button_dict = {}

        for place, events in self._event.get_all_buttons(
            start_date=st.session_state.start_datetime,
            end_date=st.session_state.end_datetime,
            room=st.session_state.room,
        ).items():
            interval = sum(calculate_index(event.start_date, event.end_date) for event in events)

            if interval < full_interval and not st.session_state.all_day:
                button_dict[int(place)] = "gold"
            else:
                button_dict[int(place)] = "red"

        return button_dict

    def button_widget(self, offset: int):
        colls = [i for i in st.columns([1, 1, 1, 9])]
        style = ""
        len_colls = len(colls)
        places_count = ROOMS[st.session_state.room]["places"]
        reserved_places = self._get_reserved_places()

        for y, col in enumerate(colls):
            with col:
                x = 1
                for i in range((y * (places_count // len_colls)) + 1, ((places_count // len_colls) * (y + 1)) + 1):
                    st.button(f"Место {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                    if i in reserved_places:
                        style += set_style_button(
                            reserved_places[i],
                            x=x,
                            y=y + 1,
                            offset=offset,
                        )
                    else:
                        style += set_style_button(
                            "green",
                            x=x,
                            y=y + 1,
                            offset=offset,
                        )

                    x += 1
                if y == (len_colls - 1) and places_count % len_colls != 0:
                    for i in range(((places_count // len_colls) * (y + 1)) + 1, places_count + 1):
                        st.button(f"Место {i}", key=f"button{i}", on_click=self.btn_callback, args=(i,))
                        if i in reserved_places:
                            style += set_style_button(
                                reserved_places[i],
                                x=x,
                                y=y + 1,
                                offset=offset,
                            )
                        else:
                            style += set_style_button(
                                "green",
                                x=x,
                                y=y + 1,
                                offset=offset,
                            )
                        x += 1

        st.markdown(
            f"""<style>
            {style}
        </style>""",
            unsafe_allow_html=True,
        )

    def set_room(self):
        if ROOMS[st.session_state.room]["places"] < int(st.session_state.place):
            st.session_state.place = "1"

    def input_email(self):

        _, col2, _ = st.columns(3)
        with col2:
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
                st.session_state.email = email.strip().lower()
                return
            else:
                st.warning("Введите пожалуйста корректный email или обратитесь в службу поддержки sa@novardis.com")
                st.stop()

    def booking(self):
        st.caption("Бронирование:")
        self._update_start_end_date()
        st.markdown(
            f"""
            ```python
            Комната: {st.session_state.room} Место: {st.session_state.place}
            Начало: {to_readable_format(st.session_state.start_datetime)}
            Конец: {to_readable_format(st.session_state.end_datetime)}
            ```
        """
        )

    def status(self):
        status = [
            self.conversion_item(item)
            for item in self._event.get_all(
                room=st.session_state.room,
                place=st.session_state.place,
                start_date=st.session_state.start_datetime,
                end_date=st.session_state.end_datetime,
            )
        ]
        st.caption("Текущий статус:")
        st.markdown(
            f"""
            ```python
            {''.join(status) or f'Бронирований места №{st.session_state.place} на выбранные даты нет'}
            """
        )
