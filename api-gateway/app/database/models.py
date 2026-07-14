from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from app.database.connection import Base


class Audit(Base):

    __tablename__ = "audits"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    audit_id = Column(
        String,
        unique=True,
        index=True
    )


    website = Column(
        String
    )


    keyword = Column(
        String,
        nullable=True
    )


    status = Column(
        String
    )


    results = Column(
        JSON
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )