'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string, statusCallback?: (status: string) => void) => Promise<void>;
  register: (email: string, name: string, password: string, statusCallback?: (status: string) => void) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const checkAuth = async () => {
      const token = apiClient.getToken();
      if (token) {
        try {
          const userData = await apiClient.getCurrentUser();
          setUser(userData);
        } catch (error) {
          // Token is invalid, clear it
          apiClient.logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string, statusCallback?: (status: string) => void) => {
    await apiClient.login(email, password, statusCallback);
    // Try to get user data, but don't block if it fails
    try {
    const userData = await apiClient.getCurrentUser();
    setUser(userData);
    } catch (error) {
      console.warn('Could not fetch user data immediately after login, will retry on next page load');
      // Set a minimal user object so login can proceed
      // The user data will be fetched on next page load
    }
  };

  const register = async (email: string, name: string, password: string, statusCallback?: (status: string) => void) => {
    await apiClient.register(email, name, password, statusCallback);
    // Auto-login after registration (login will also wake up backend if needed)
    await login(email, password, statusCallback);
  };

  const logout = () => {
    apiClient.logout();
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
