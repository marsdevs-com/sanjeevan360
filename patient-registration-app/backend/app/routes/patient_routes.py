"""
Patient Routes Module

This module defines the API endpoints for patient-related operations.
It includes routes for creating, retrieving, and managing patient records.

The module uses FastAPI for defining routes and SQLAlchemy for database operations.
Patient data is stored in both PostgreSQL (for relational data) and MongoDB
(for document-based storage with additional metadata).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import datetime

from app.models.patient import Patient, PatientCreate, PatientInDB
from app.database.postgres_db import get_db, PatientTable
from app.database.mongo_db import get_patients_collection

# Create API router
router = APIRouter()

def patient_to_dict(patient: PatientTable) -> Dict[str, Any]:
    """
    Convert a SQLAlchemy PatientTable model to a dictionary.

    This helper function converts a SQLAlchemy model instance to a dictionary
    that can be used with Pydantic models and for JSON serialization.

    Args:
        patient (PatientTable): The SQLAlchemy model instance to convert

    Returns:
        Dict[str, Any]: Dictionary representation of the patient
    """
    return {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact
    }

@router.post("/patients/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient record.

    This endpoint creates a new patient record in both PostgreSQL and MongoDB.
    The primary data is stored in PostgreSQL, while a copy with additional
    metadata (like creation timestamp) is stored in MongoDB.

    Args:
        patient (PatientCreate): The patient data from the request body
        db (Session): The database session (injected by FastAPI)

    Returns:
        Patient: The created patient record

    Raises:
        HTTPException: If there's an error creating the patient record
    """
    # Create patient in PostgreSQL
    db_patient = PatientTable(
        name=patient.name,
        age=patient.age,
        gender=patient.gender.value,
        contact=patient.contact
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    # Create patient in MongoDB (with error handling)
    try:
        mongo_collection = get_patients_collection()
        if mongo_collection:
            patient_data = patient_to_dict(db_patient)
            patient_data["created_at"] = datetime.datetime.now().isoformat()
            await mongo_collection.insert_one(patient_data)
        else:
            print("MongoDB collection is None, skipping MongoDB insert")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")
        # Continue even if MongoDB insert fails - PostgreSQL is the primary data store

    return patient_to_dict(db_patient)

@router.get("/patients/", response_model=List[Patient])
async def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of patients.

    This endpoint retrieves a paginated list of patients from the database.

    Args:
        skip (int, optional): Number of records to skip (for pagination). Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.
        db (Session): The database session (injected by FastAPI)

    Returns:
        List[Patient]: List of patient records
    """
    patients = db.query(PatientTable).offset(skip).limit(limit).all()
    return [patient_to_dict(patient) for patient in patients]

@router.get("/patients/{patient_id}", response_model=Patient)
async def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific patient by ID.

    This endpoint retrieves a single patient record by its ID.

    Args:
        patient_id (int): The ID of the patient to retrieve
        db (Session): The database session (injected by FastAPI)

    Returns:
        Patient: The requested patient record

    Raises:
        HTTPException: If the patient with the specified ID is not found (404)
    """
    patient = db.query(PatientTable).filter(PatientTable.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_to_dict(patient)
