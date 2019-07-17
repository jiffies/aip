from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from database import Base

class Plan(Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    total_invest_money = Column(Integer, default=0)
    content = Column(JSON)
    created_at = Column(DateTime, nullable=False,
                        default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

