from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.db import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    costs = relationship("CostModel", back_populates="user")