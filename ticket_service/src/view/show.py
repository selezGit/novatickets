import streamlit as st
from core.utils import to_readable_format
from models import Event

from view.base import BaseView


class ShowView(BaseView):
    @st.cache
    def conversion_item(self, item: Event) -> str:
        return f"""
        Комната: {item.room} Место: {item.place} Забронировал: {item.creator}
        {to_readable_format(item.start_date)} - Начальная дата и время
        {to_readable_format(item.end_date)} - Конечная дата и время
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
