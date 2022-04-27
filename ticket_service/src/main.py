import subprocess

from core.config import CONSUMER_PORT
from db.postgres import init_db

if __name__ == "__main__":
    init_db()

    subprocess.Popen(
        [
            "streamlit",
            "run",
            "run_streamlit.py",
        ]
    )
    subprocess.Popen(
        [
            "/bin/sh",
            "-c",
            f"uwsgi --socket 0.0.0.0:{CONSUMER_PORT} --protocol=http -w  wsgi:app",
        ]
    )
