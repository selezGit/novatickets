import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + os.sep
TEMPLATE_DIR = BASE_DIR + "src" + os.sep + "templates" + os.sep

# email conf
SENDER_MAIL = os.getenv("SENDER_MAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")


# Redis conf
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASS = os.getenv("REDIS_PASS", "")
CACHE_EXPIRE_IN_SECONDS = 60 * 60 * 24


# Postgresql
DB = {
    "DIALECT": os.getenv("DB_DIALECT", "postgresql+psycopg2"),
    "HOST": os.getenv("DB_HOST"),
    "PORT": os.getenv("DB_PORT"),
    "NAME": os.getenv("DB_NAME"),
    "USER": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
}

# app settings
ROOMS = {
    "97.1": {"places": 14},
    "90": {"places": 21},
}

COLORS = {
    "green": "#00FF00",
    "yellow": "#FFFF00",
    "red": "#FF0000",
}

WHITE_LIST = [".com", ".ru"]
MANAGERS = []
MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD")


CONSUMER_HOST = os.getenv("CONSUMER_HOST")
CONSUMER_PORT = os.getenv("CONSUMER_PORT")

CACHE_URL = f"http://{CONSUMER_HOST}:{CONSUMER_PORT}/confirm?key="

OPERATIONS = {
    "change": "изменения",
    "create": "подтверждения",
    "delete": "отмены",
}

MSG_TEMPLATE = {
    "create": "Бронирование успешно подтверждено.",
    "change": "Бронирование успешно изменено.",
    "delete": "Отмена бронирования успешно произведена.",
}

TIME = [
    "00:00",
    "00:30",
    "01:00",
    "01:30",
    "02:00",
    "02:30",
    "03:00",
    "03:30",
    "04:00",
    "04:30",
    "05:00",
    "05:30",
    "06:00",
    "06:30",
    "07:00",
    "07:30",
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
    "22:00",
    "22:30",
    "23:00",
    "23:30",
    "23:59",
]


STREAMLIT_STYLES = """ <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """

try:
    from .local import *
except ImportError:
    pass
