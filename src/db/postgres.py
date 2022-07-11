from core.config import DB
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = URL(
    drivername=DB["DIALECT"],
    username=DB["USER"],
    password=DB["PASSWORD"],
    host=DB["HOST"],
    port=DB["PORT"],
    database=DB["NAME"],
)

engine = create_engine(db_url)

Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


def init_db():
    from models import event  # noqa

    Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
