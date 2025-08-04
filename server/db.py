from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=300,  # Recycle connections after 5 minutes
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print(f"Database connection successful: {settings.DATABASE_URL}")
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise e
