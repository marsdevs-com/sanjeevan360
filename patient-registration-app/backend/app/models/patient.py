"""
Patient Models Module

This module defines the Pydantic models for patient data validation and serialization.
These models are used for request/response validation and documentation in the API.

The module includes models for:
- Base patient data (common fields)
- Patient creation (input data)
- Patient response (output data)
- Patient database representation (with additional fields)
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    """
    Enum for patient gender options.

    This enum defines the valid gender options for patients in the system.
    It inherits from str to ensure the values are stored as strings.
    """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class PatientBase(BaseModel):
    """
    Base model for patient data.

    This model defines the common fields for all patient-related models.
    It includes validation rules for each field to ensure data integrity.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Patient's full name (2-100 characters)"
    )
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        description="Patient's age in years (1-149)"
    )
    gender: GenderEnum = Field(
        ...,
        description="Patient's gender (male, female, or other)"
    )
    contact: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Patient's contact information (5-20 characters)"
    )

class PatientCreate(PatientBase):
    """
    Model for patient creation requests.

    This model is used for validating the request body when creating a new patient.
    It inherits all fields from PatientBase without adding any new fields.
    """
    pass

class Patient(PatientBase):
    """
    Model for patient responses.

    This model is used for the response body when returning patient data.
    It includes all fields from PatientBase plus the patient ID.
    """
    id: int = Field(..., description="Unique identifier for the patient")

    class Config:
        """Configuration for the Patient model."""
        orm_mode = True  # Allows the model to work with ORM objects

class PatientInDB(Patient):
    """
    Model for patient data as stored in the database.

    This model represents how patient data is stored in the database.
    It includes all fields from Patient plus additional metadata fields.
    """
    # Additional fields that might be stored in the database
    created_at: Optional[str] = Field(
        None,
        description="Timestamp when the patient record was created"
    )
    updated_at: Optional[str] = Field(
        None,
        description="Timestamp when the patient record was last updated"
    )
