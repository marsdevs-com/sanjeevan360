/**
 * API Service Module
 *
 * This module provides a centralized interface for making API requests to the backend.
 * It uses axios for HTTP requests and includes functions for all patient-related operations.
 *
 * The module configures a base axios instance with the appropriate URL and headers,
 * and exports specific functions for each API endpoint.
 */

import axios from 'axios';

// Get API URL from environment variables or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Configured axios instance for API requests
 *
 * This instance is pre-configured with:
 * - Base URL from environment variables
 * - JSON content type header
 * - Default request timeout
 */
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

/**
 * Patient API functions
 *
 * This object contains all functions related to patient operations:
 * - registerPatient: Create a new patient record
 * - getPatients: Retrieve a list of all patients
 * - getPatient: Retrieve a specific patient by ID
 */
export const patientApi = {
  /**
   * Register a new patient
   *
   * Sends a POST request to create a new patient record in the database.
   *
   * @param {Object} patientData - The patient data to register
   * @param {string} patientData.name - Patient's full name
   * @param {number} patientData.age - Patient's age
   * @param {string} patientData.gender - Patient's gender (male, female, other)
   * @param {string} patientData.contact - Patient's contact information
   * @returns {Promise<Object>} The created patient record with ID
   * @throws {Error} If the API request fails
   */
  registerPatient: async (patientData) => {
    try {
      const response = await api.post('/patients/', patientData);
      return response.data;
    } catch (error) {
      console.error('Error registering patient:', error);
      throw error;
    }
  },

  /**
   * Get all patients
   *
   * Retrieves a list of all patients from the database.
   *
   * @returns {Promise<Array>} Array of patient objects
   * @throws {Error} If the API request fails
   */
  getPatients: async () => {
    try {
      const response = await api.get('/patients/');
      return response.data;
    } catch (error) {
      console.error('Error fetching patients:', error);
      throw error;
    }
  },

  /**
   * Get a specific patient by ID
   *
   * Retrieves a single patient record by its ID.
   *
   * @param {number} id - The ID of the patient to retrieve
   * @returns {Promise<Object>} The requested patient record
   * @throws {Error} If the API request fails or the patient is not found
   */
  getPatient: async (id) => {
    try {
      const response = await api.get(`/patients/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching patient with ID ${id}:`, error);
      throw error;
    }
  },
};

export default api;
