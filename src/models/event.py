import uuid

from db.postgres import Base
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

MAX_DB_STRING_LENGTH = 255


class Event(Base, SerializerMixin):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    creator = Column(String(MAX_DB_STRING_LENGTH))
    room = Column(String(MAX_DB_STRING_LENGTH))
    place = Column(String(MAX_DB_STRING_LENGTH))

    def __repr__(self):
        return f"<Event for user: {self.creator} uid: {self.uid}>"
