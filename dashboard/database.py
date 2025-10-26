from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///tracker.db', pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)
Base = declarative_base()
