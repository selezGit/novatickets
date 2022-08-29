import time
import streamlit as st
from core.utils import format_events

from view.base import BaseView


class DeleteView(BaseView):
    def main_delete(self):
        events = self._event.get_by_email(creator=st.session_state.email)
        if events:
            col1, _ = st.columns([3, 1])
            with col1:
                selected_events = st.multiselect(
                    "Выберите события для отмены",
                    events,
                    format_func=lambda x: format_events(x),
                )
                submit = st.button("Удалить выбранные события")
                if submit:
                    if not selected_events:
                        st.stop()

                    self._event.delete(selected_events)

                    st.success("✅ Бронирование отменено")
                    time.sleep(1)
                    st.experimental_rerun()

        else:
            st.warning("⚠️ События не найдены, попробуйте добавить их на вкладке 'Создать'")
