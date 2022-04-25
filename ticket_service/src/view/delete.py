import streamlit as st

from view.base import BaseView


class DeleteEvent(BaseView):
    def main_delete(self):
        st.session_state.num = 1
        while True:
            placeholder = st.empty()
            placeholder2 = st.empty()

            with placeholder.container():
                events = self._event.get_by_email(creator=st.session_state.email)
                if events:
                    st.subheader("Выберите события для удаления")
                    selected_events = st.multiselect(
                        "Please select events for remove",
                        events,
                        key=f"selected{st.session_state.num}",
                        format_func=lambda x: self.format_events(x),
                    )
                    submit = st.button("Удалить выбранные события", key=st.session_state.num)
                    if submit:
                        if not selected_events:
                            st.stop()
                        with st.spinner("Please wait..."):
                            self._event.delete(st.session_state.email, selected_events)

                            placeholder2.success(
                                "На указанный email отправлено письмо для подтверждения отмены бронирования"
                            )
                            st.session_state.num += 1
                            placeholder.empty()
                    else:
                        st.stop()

                else:
                    st.warning(
                        "События не найдены, попробуйте ввести корректный email или добавить события на вкладке Add"
                    )
                    break
