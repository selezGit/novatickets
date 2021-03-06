import streamlit as st
from core.config import BASE_DIR
from PIL import Image

from view.base import BaseView


class FAQView(BaseView):
    @st.cache
    def open_image(self, name: str):
        return Image.open(BASE_DIR + f"src/static/img/{name}")

    def main_faq(self):
        st.title("FAQ", anchor="main")
        st.markdown(
            """ 
        ##### 1. [Забронировать рабочее место](#Create)
        ##### 2. [Забронировать несколько рабочих мест](#Create_all)
        ##### 3. [Изменить бронирование](#Change)
        ##### 4. [Отменить бронирование](#Delete)
        """
        )

        st.markdown("---")
        st.subheader("Забронировать рабочее место", anchor="Create")
        st.markdown(
            "1. На панели слева нажмите , а затем выберите нужные: **дату**, **время**, **кабинет**, **место**."
        )
        st.image(self.open_image("create_btn.png"))
        st.markdown("##### ***Справа отображается текущий статус, выбранного места***!")
        st.image(self.open_image("create_window.png"))
        st.write(f"2. Нажмите")
        st.image(self.open_image("booking_btn.png"))
        st.write("3. В почте найдите письмо с подтверждением, нажмите")
        st.image(self.open_image("apply_btn.png"))
        st.image(self.open_image("create_mail.png"))

        st.markdown("---")
        st.subheader("Забронировать несколько рабочих мест", anchor="Create_all")
        st.markdown(
            "1. На панели слева нажмите , а затем выберите нужные: **дату**, **время**, **кабинет**, **место**."
        )
        st.image(self.open_image("create_btn.png"))
        st.markdown("##### ***Справа отображается текущий статус, выбранного места***!")
        st.image(self.open_image("create_window.png"))
        st.markdown("2. Для добавления нескольких бронирований за раз, нужно нажать на кнопку '+'")
        st.image(self.open_image("add_events_btn.png"))
        st.write(f"3. Нажмите")
        st.image(self.open_image("booking_btn.png"))
        st.write("4. В почте найдите письмо с подтверждением, нажмите")
        st.image(self.open_image("apply_btn.png"))
        st.image(self.open_image("create_mail.png"))

        st.markdown("---")
        st.subheader("Изменить бронирование", anchor="Change")
        st.write("1. Для для изменения бронирования нажмите нажмите")
        st.image(self.open_image("change_btn.png"))
        st.write("2. Выберите нужное событие в выпадающем меню")
        st.image(self.open_image("change_window.png"))
        st.write("3. Нажмите")
        st.image(self.open_image("change_btn2.png"))
        st.write("4. В почте найдите письмо с подтверждением, нажмите")
        st.image(self.open_image("apply_btn.png"))
        st.image(self.open_image("change_mail.png"))

        st.markdown("---")
        st.subheader("Отменить бронирование", anchor="Delete")
        st.write("1. Для отмены бронирования нажмите")
        st.image(self.open_image("delete_btn.png"))
        st.write("2. Нажмите")
        st.image(self.open_image("delete_btn2.png"))
        st.write("3. В почте найдите письмо с подтверждением, нажмите")
        st.image(self.open_image("apply_btn.png"))
        st.image(self.open_image("delete_mail.png"))
