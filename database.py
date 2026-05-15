from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite database — creates a file called "books.db" in your project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Engine = the connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite only
)

# SessionLocal = a factory that creates new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = parent class for all database models (tables)
class Base(DeclarativeBase):
    pass
