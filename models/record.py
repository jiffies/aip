from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from database import Base

class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer)
    content = Column(JSON)
    created_at = Column(DateTime, nullable=False,
                        default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

