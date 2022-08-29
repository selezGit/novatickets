import asyncio
from typing import Dict

import streamlit as st
from bokeh.models.widgets import Div
from core.config import *
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2


class MSOauthService:
    def __init__(self):
        self.client = MicrosoftGraphOAuth2(
            CLIENT_ID,
            CLIENT_SECRET,
            TENANT,
        )

    async def write_authorization_url(self) -> str:
        """Функция запроса url авторизации"""
        authorization_url = await self.client.get_authorization_url(
            REDIRECT_URI,
            scope=SCOPE,
            extras_params={"access_type": "offline"},
        )
        return authorization_url

    async def write_access_token(self, code):
        """функция запроса access токена"""
        token = await self.client.get_access_token(code, REDIRECT_URI)
        return token

    async def redirect_to(self, url):
        """функция перенаправления на url"""
        js = f"window.location.href = '{url}'"
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

    async def get_userdata(self, token) -> Dict[str, str]:
        """извлекает данные о пользователе"""
        user_data = await self.client.get_id_email(token)
        return user_data

    def login(self) -> None:
        """создаёт ссылку для авторизации, и перенаправляет на сервис авторизации по нажатии на кнопку"""
        authorization_url = asyncio.run(self.write_authorization_url())
        asyncio.run(self.redirect_to(authorization_url))

    def logout(self) -> None:
        """выход из УЗ"""
        asyncio.run(self.redirect_to(LOGOUT_URL))

    def authorizate(self, code: dict) -> None:
        st.session_state.token = asyncio.run(
            self.write_access_token(
                code=code["code"],
            )
        )
        st.experimental_set_query_params()

    def handler_get_userdata(self) -> Dict[str, str]:
        """синхронная обёртка для вызова асинхронной функции"""
        return asyncio.run(self.get_userdata(token=st.session_state.token["access_token"]))

    def __call__(self):
        """Основной метод прохождения авторизации"""
        if not "token" in st.session_state:
            st.session_state.token = {}

        code = st.experimental_get_query_params()
        if code:
            self.authorizate(code)
