import api from './api';
import { User, AuthResponse, RegisterRequest } from '../types/auth';

export const authService = {
  async login(username: string, password: string): Promise<{ token: string; user: User }> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post<AuthResponse>('/api/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const token = response.data.access_token;
    
    // Get user data
    const userResponse = await api.get<User>('/api/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return {
      token,
      user: userResponse.data,
    };
  },

  async register(userData: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/api/auth/register', userData);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  },
};
