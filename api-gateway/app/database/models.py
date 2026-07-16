from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float

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
        String,
        default="pending"
    )


    results = Column(
        JSON,
        default={}
    )


    error_message = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    started_at = Column(
        DateTime,
        nullable=True
    )


    completed_at = Column(
        DateTime,
        nullable=True
    )


    execution_time = Column(
        Float,
        nullable=True
    )





class Module(Base):

    __tablename__ = "modules"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )


    url = Column(
        String,
        nullable=False
    )


    description = Column(
        String,
        nullable=True
    )


    active = Column(
        Boolean,
        default=True
    )


    priority = Column(
        Integer,
        default=100
    )


    timeout = Column(
        Integer,
        default=30
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )