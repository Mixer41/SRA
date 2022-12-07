from sqlalchemy import Column, Integer, String
from database import Base


class Appeal(Base):
    __tablename__ = "appeal"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone = Column(String)
    appeal = Column(Integer)