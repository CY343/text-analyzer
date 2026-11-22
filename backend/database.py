from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./analyzer.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind = engine, autoflush=False)
Base = declarative_base()

class Analysis(Base):
  __tablename__ = "analyses"

  id = Column(Integer, primary_key = True, index = True)
  text = Column(String, nullable=False)
  label = Column(String, nullable=False)
  score = Column(Float, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)