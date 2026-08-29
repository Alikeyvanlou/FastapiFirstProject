from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    costs = relationship("CostModel", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("RefreshTokenModel", back_populates="user", cascade="all, delete-orphan")
