"""
MongoDB Database Connection Module

This module provides functionality for connecting to MongoDB and accessing
collections. It uses the motor library for asynchronous MongoDB operations.

The module initializes a connection to MongoDB on application startup and
provides functions to access the database and collections.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# MongoDB connection string from environment variable or default for development
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "patient_db")

# MongoDB client and database instances (initialized in init_mongodb)
client = None
db = None

async def init_mongodb():
    """
    Initialize the MongoDB connection.

    This function creates an AsyncIOMotorClient instance and connects to the
    specified MongoDB database. It verifies the connection with a ping command.

    The function sets the global client and db variables that are used by
    other functions in this module.

    Raises:
        ConnectionFailure: If the connection to MongoDB fails
    """
    global client, db
    try:
        # Create AsyncIOMotorClient instance
        client = AsyncIOMotorClient(MONGO_URL)

        # Verify connection by sending a ping command to the server
        await client.admin.command('ping')

        # Get database instance
        db = client[DB_NAME]
        print("Connected to MongoDB")
    except ConnectionFailure:
        print("MongoDB connection failed")
        # In a production environment, you might want to implement retry logic
        # or raise an exception to prevent the application from starting

def get_mongodb():
    """
    Get the MongoDB database instance.

    Returns:
        AsyncIOMotorDatabase: The MongoDB database instance, or None if not connected
    """
    return db

def get_patients_collection():
    """
    Get the patients collection from MongoDB.

    This function returns the 'patients' collection from the MongoDB database.
    It's used to perform CRUD operations on patient documents.

    Returns:
        AsyncIOMotorCollection: The patients collection, or None if not connected
    """
    return db.patients if db else None

async def close_mongodb_connection():
    """
    Close the MongoDB connection.

    This function should be called when the application is shutting down
    to properly close the MongoDB connection.
    """
    if client:
        client.close()
        print("MongoDB connection closed")
