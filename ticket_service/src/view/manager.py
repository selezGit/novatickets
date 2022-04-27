import streamlit as st
from services.auth import AuthService

from view.base import BaseView


class ManagerView(BaseView):

    _auth = AuthService()

    def check_password(self):
        """Returns `True` if the user had the correct password."""

        def password_entered():
            """Checks whether a password entered by the user is correct."""

            if self._auth.check_password(st.session_state["password"]):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            # First run, show input for password.
            st.text_input("Password", type="password", on_change=password_entered, key="password")
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            st.text_input("Password", type="password", on_change=password_entered, key="password")
            st.error("😕 Password incorrect")
            return False
        else:
            # Password correct.
            return True

    def main_manager(self):
        self.check_password()
