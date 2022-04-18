import uuid

from db.postgres import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

MAX_DB_STRING_LENGTH = 255


class Event(Base):
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
    is_cancelled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Event for user: {self.creator} uid: {self.uid}>"
