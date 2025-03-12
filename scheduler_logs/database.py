from sqlalchemy import create_engine, Column, DateTime, Text, Integer, String  # Added String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

# REPLACE WITH YOUR ACTUAL CREDENTIALS!
DATABASE_URL = 'mysql+pymysql://root:NiGr%408120@localhost/scheduler'

Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'  # Corrected: Use __tablename__
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    log_type = Column(String(50))  # Added log_type column
    log_message = Column(Text)

engine = create_engine(DATABASE_URL)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()