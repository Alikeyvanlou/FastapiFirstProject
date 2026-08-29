from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_engine(settings.database_url)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
