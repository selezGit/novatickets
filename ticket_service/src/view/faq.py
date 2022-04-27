from pathlib import Path

import streamlit as st

from view.base import BaseView


class FAQView(BaseView):
    def read_markdown_file(self, markdown_file):
        return Path(markdown_file).read_text()

    def main_faq(self):
        st.markdown(
            """
        # FAQ
        Тут будут инструкции и обучающие видео"""
        )
