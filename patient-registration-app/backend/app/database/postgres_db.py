"""
PostgreSQL Database Connection Module

This module provides functionality for connecting to PostgreSQL and defining
the database models. It uses SQLAlchemy as the ORM (Object-Relational Mapping)
library.

The module initializes a connection to PostgreSQL on application startup,
defines the database models, and provides a function to get a database session.
"""

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
import os
from typing import AsyncGenerator

# Database URL from environment variable or default for development
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@postgres:5432/patient_db")

# Create SQLAlchemy engine and session factory
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Gender(str, enum.Enum):
    """
    Enum for patient gender options.

    This enum defines the valid gender options for patients in the system.
    It inherits from str to ensure the values are stored as strings in the database.
    """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class PatientTable(Base):
    """
    SQLAlchemy model for the patients table.

    This class defines the structure of the patients table in PostgreSQL.
    It includes columns for patient information such as name, age, gender, and contact.
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True,
                doc="Unique identifier for the patient")
    name = Column(String, index=True,
                 doc="Patient's full name")
    age = Column(Integer,
                doc="Patient's age in years")
    gender = Column(String,
                   doc="Patient's gender (male, female, or other)")
    contact = Column(String,
                    doc="Patient's contact information (phone number)")

async def init_postgres():
    """
    Initialize the PostgreSQL database.

    This function creates all tables defined by the SQLAlchemy models
    if they don't already exist in the database.
    """
    Base.metadata.create_all(bind=engine)

async def get_db() -> AsyncGenerator:
    """
    Get a database session.

    This function creates a new SQLAlchemy session and yields it to the caller.
    The session is automatically closed when the caller is done with it.

    Yields:
        Session: A SQLAlchemy session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
