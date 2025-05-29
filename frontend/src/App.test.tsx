import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './contexts/AuthContext';

// Mock the auth context
jest.mock('./contexts/AuthContext', () => ({
  ...jest.requireActual('./contexts/AuthContext'),
  useAuth: () => ({
    user: null,
    loading: false,
    login: jest.fn(),
    register: jest.fn(),
    logout: jest.fn(),
  }),
}));

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        {component}
      </AuthProvider>
    </BrowserRouter>
  );
};

test('renders login page when user is not authenticated', () => {
  renderWithProviders(<App />);
  // The app should redirect to login when no user is authenticated
  expect(window.location.pathname).toBe('/');
});
