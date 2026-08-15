from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///database.db')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Cost(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key = True)
    description = Column(String)
    amount = Column(Float)
