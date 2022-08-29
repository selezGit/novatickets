from db.postgres import init_db
from view.main_view import ViewApp

if __name__ == "__main__":
    init_db()
    view = ViewApp()
    view.run()
