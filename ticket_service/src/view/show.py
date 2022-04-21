import streamlit as st
from models import Event

from view.base import BaseView


class ShowEvents(BaseView):
    @st.cache
    def conversion_item(self, item: Event) -> str:
        return f"""
        Комната: {item.room} Место: {item.place} Забронировал: {item.creator}
        {item.start_date.strftime("%d.%m.%Y %H:%M")} - Начальная дата и время
        {item.end_date.strftime("%d.%m.%Y %H:%M")} - Конечная дата и время
         """

    def show_form(self):
        start, end = self.combine_datetime()
        status = [
            self.conversion_item(item)
            for item in self._event.get_all(
                room=st.session_state.room,
                place=st.session_state.selected,
                start_date=start,
                end_date=end,
            )
        ]

        st.subheader("status")
        st.markdown(
            f"""
            ```python
            {''.join(status) or f'Бронирований места №{st.session_state.selected} на выбранные даты нет'}
            """
        )

    def main_show(self):
        self.side_bar()
        self.show_form()
        with st.expander(f"Room {st.session_state.room}", expanded=False):
            st.image(
                self.get_image(st.session_state.room),
            )
