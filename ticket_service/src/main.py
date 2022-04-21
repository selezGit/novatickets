import subprocess
from db.postgres import init_db


if __name__ == "__main__":
    init_db()

    subprocess.Popen(["streamlit", "run", "run_streamlit.py"])
    subprocess.Popen(["python", "run_consumer.py"])
