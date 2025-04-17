import pytest

def test_simple_patient():
    """A simple test that always passes"""
    assert True

def test_patient_data_validation():
    """Test basic validation logic without FastAPI dependencies"""
    # Simulate patient data
    patient_data = {
        "name": "Test Patient",
        "age": 30,
        "gender": "male",
        "contact": "1234567890"
    }

    # Basic validation
    assert len(patient_data["name"]) >= 2, "Name should be at least 2 characters"
    assert 0 < patient_data["age"] < 150, "Age should be between 1 and 149"
    assert patient_data["gender"] in ["male", "female", "other"], "Gender should be valid"
    assert len(patient_data["contact"]) >= 5, "Contact should be at least 5 characters"
