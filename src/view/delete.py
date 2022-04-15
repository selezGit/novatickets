import streamlit as st
from core.config import *

from view.base import BaseView


class DeleteEvent(BaseView):
    @st.cache
    def format_events(self, event):
        return f"from {self.to_readable_format(event.start_date)} to {self.to_readable_format(event.end_date)} Комната: {event.room} место: {event.place}"

    def delete_form(self, events):
        if events:
            with st.form("Step 1"):
                selected_events = st.multiselect(
                    "Please select events",
                    events,
                    key="selected_events",
                    format_func=lambda x: self.format_events(x),
                )
                if st.form_submit_button("Submit"):
                    [self._event.delete(event.uid) for event in selected_events]
                    st.success("На указанный email отправлено письмо для удаления события")

    def main_delete(self):
        self.side_bar()

        email = st.text_input(
            "Введите email",
        )

        if email:
            events = self._event.get_by_email(creator=email)
            if events:
                self.delete_form(events)
            else:
                st.warning("События не найдены, попробуйте ввести корректный email или добавить события на вкладке Add")
