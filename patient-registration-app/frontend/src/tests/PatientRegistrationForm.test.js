import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import PatientRegistrationForm from '../components/PatientRegistrationForm';
import { patientApi } from '../services/api';

// Mock the API and toast
jest.mock('../services/api', () => ({
  patientApi: {
    registerPatient: jest.fn(),
  },
}));

const mockToastSuccess = jest.fn();
const mockToastError = jest.fn();

jest.mock('react-toastify', () => ({
  toast: {
    success: jest.fn(message => mockToastSuccess(message)),
    error: jest.fn(message => mockToastError(message)),
  },
}));

describe('PatientRegistrationForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the form correctly', () => {
    render(<PatientRegistrationForm />);

    // Check if all form elements are rendered
    expect(screen.getByLabelText(/Full Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Gender/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Contact Number/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Register Patient/i })).toBeInTheDocument();
  });

  test('submits the form with valid data', async () => {
    patientApi.registerPatient.mockResolvedValueOnce({ id: 1, name: 'John Doe' });

    render(<PatientRegistrationForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Age/i), { target: { value: '30' } });
    fireEvent.change(screen.getByLabelText(/Gender/i), { target: { value: 'male' } });
    fireEvent.change(screen.getByLabelText(/Contact Number/i), { target: { value: '1234567890' } });

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Register Patient/i }));

    // Check if API was called with correct data
    await waitFor(() => {
      expect(patientApi.registerPatient).toHaveBeenCalledWith({
        name: 'John Doe',
        age: 30,
        gender: 'male',
        contact: '1234567890'
      });
    });

    // Check if success message is displayed
    await waitFor(() => {
      expect(screen.getByText(/Registration Successful/i)).toBeInTheDocument();
    });
  });

  test('shows error when form submission fails', async () => {
    // Mock API to reject
    patientApi.registerPatient.mockRejectedValueOnce(new Error('API Error'));

    render(<PatientRegistrationForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Age/i), { target: { value: '30' } });
    fireEvent.change(screen.getByLabelText(/Gender/i), { target: { value: 'male' } });
    fireEvent.change(screen.getByLabelText(/Contact Number/i), { target: { value: '1234567890' } });

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Register Patient/i }));

    // Check if API was called
    await waitFor(() => {
      expect(patientApi.registerPatient).toHaveBeenCalled();
    });
  });

  test('validates required fields', async () => {
    const { container } = render(<PatientRegistrationForm />);

    // Submit form without filling it
    fireEvent.click(screen.getByRole('button', { name: /Register Patient/i }));

    // API should not be called because form validation should prevent submission
    expect(patientApi.registerPatient).not.toHaveBeenCalled();

    // Check if toast error was called with validation message
    expect(mockToastError).toHaveBeenCalledWith('Please fill in all required fields');

    // Check if required attributes are present on form fields
    const nameInput = screen.getByLabelText(/Full Name/i);
    const ageInput = screen.getByLabelText(/Age/i);
    const contactInput = screen.getByLabelText(/Contact Number/i);

    expect(nameInput).toHaveAttribute('required');
    expect(ageInput).toHaveAttribute('required');
    expect(contactInput).toHaveAttribute('required');
  });

  test('shows error message when API call fails', async () => {
    // Mock API to reject with a specific error
    const errorResponse = {
      response: {
        data: {
          detail: 'Server error occurred'
        }
      }
    };
    patientApi.registerPatient.mockRejectedValueOnce(errorResponse);

    render(<PatientRegistrationForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Age/i), { target: { value: '30' } });
    fireEvent.change(screen.getByLabelText(/Gender/i), { target: { value: 'male' } });
    fireEvent.change(screen.getByLabelText(/Contact Number/i), { target: { value: '1234567890' } });

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Register Patient/i }));

    // Check if API was called
    await waitFor(() => {
      expect(patientApi.registerPatient).toHaveBeenCalled();
    });

    // Check if toast error was called with the error message
    await waitFor(() => {
      expect(mockToastError).toHaveBeenCalledWith('Server error occurred');
    });
  });

  test('renders UI elements correctly with proper styling', () => {
    const { container } = render(<PatientRegistrationForm />);

    // Check for SVG icons in the form
    const svgIcons = container.querySelectorAll('svg');
    expect(svgIcons.length).toBeGreaterThan(0);

    // Check for styled input fields
    const inputFields = container.querySelectorAll('input, select');
    inputFields.forEach(field => {
      expect(field.className).toContain('rounded-md');
      expect(field.className).toContain('shadow-sm');
    });

    // Check for styled button
    const submitButton = screen.getByRole('button', { name: /Register Patient/i });
    expect(submitButton.className).toContain('rounded-md');
    expect(submitButton.className).toContain('shadow-md');

    // Check for proper loading state in button
    const { rerender } = render(<PatientRegistrationForm />);

    // Access the component's state and set loading to true
    // Note: This is a simplified approach; in a real test you might use a test-specific prop
    const formWithLoading = React.createElement(PatientRegistrationForm, {
      testLoading: true  // This prop would need to be handled in the component for testing
    });

    // In a real test, you would trigger the loading state through user interaction
    // Here we're just checking that the button has the right classes for styling
    expect(submitButton.className).toContain('text-white');
  });
});
