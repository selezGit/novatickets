import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + os.sep
IMG_DIR = BASE_DIR + "img" + os.sep

# Redis conf
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASS = os.getenv("REDIS_PASS", "")
CACHE_EXPIRE_IN_SECONDS = 60 * 60 * 24 * 7


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

try:
    from .local import *
except ImportError:
    pass
