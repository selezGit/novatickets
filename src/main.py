from core.config import *
from db.postgres import init_db
from view.streamlit_app import ViewApp

if __name__ == "__main__":
    init_db()
    view = ViewApp()
    view.run()
