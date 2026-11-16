from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TenderDB(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tender_number = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    customer = Column(String(300))
    description = Column(Text)
    cpv_code = Column(String(50), index=True)
    status = Column(String(100))
    budget = Column(Float, nullable=True)
    currency = Column(String(10), default="GEL")
    deadline = Column(DateTime, nullable=True)
    source_url = Column(String(500), nullable=False)
    platform = Column(String(50))
    is_relevant = Column(Boolean, default=False)
    relevance_reason = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)