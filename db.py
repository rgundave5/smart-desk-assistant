from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connect to your existing SQLite database file
engine = create_engine('sqlite:///app/tracker.db', echo=True)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Base class for declarative class definitions
Base = declarative_base()
