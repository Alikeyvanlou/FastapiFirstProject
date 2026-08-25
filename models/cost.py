from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class CostModel(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    amount = Column(Float)
    create_at = Column(String)
    update_at = Column(String, default = None)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="costs")