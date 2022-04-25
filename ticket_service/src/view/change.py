import streamlit as st

from view.base import BaseView


class ChangeEvent(BaseView):
    def change_form(self, events):
        start, end = self.combine_datetime()
        st.markdown(
            f"""
            ##### **Новая дата**
            ```python
            Комната: {st.session_state.room} Место: {st.session_state.selected}
            {start.strftime("%d.%m.%Y %H:%M")} - Начальная дата и время
            {end.strftime("%d.%m.%Y %H:%M")} - Конечная дата и время
            ```
            ##### Выберите событие для изменения
        """
        )

        with st.form("Step 1"):
            selected_event = st.selectbox(
                "Please select events for change",
                events,
                format_func=lambda x: self.format_events(x),
            )
            submit = st.form_submit_button("Изменить событие")
            if submit:
                with st.spinner("Please wait..."):
                    if self._event.change(
                        email=st.session_state.email,
                        instance=selected_event,
                        start_date=start,
                        end_date=end,
                        creator=st.session_state.email,
                        room=st.session_state.room,
                        place=str(st.session_state.selected),
                    ):
                        st.success("На указанный email отправлено письмо для подтверждения изменения бронирования")
                    else:
                        st.error(f"Рабочее место №{st.session_state.selected} на указанную дату уже занято")

    def main_change(self):
        self.side_bar()
        events = self._event.get_by_email(creator=st.session_state.email)
        if events:
            self.change_form(events)

        else:
            st.warning("События не найдены, попробуйте ввести корректный email или добавить события на вкладке Add")
