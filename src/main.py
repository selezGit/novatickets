from core.config import *
from view.streamlit_app import ViewApp
from db.postgres import init_db

if __name__ == "__main__":

    init_db()

    view = ViewApp()

    view.run()
