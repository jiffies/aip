from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from database import Base
import datetime


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    content = Column(JSON)
    period = Column(JSON)
    money = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
