from sqlalchemy import Integer, String, Column
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String, nullable=False)
