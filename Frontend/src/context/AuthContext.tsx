import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, TokenResponse } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (tokenResponse: TokenResponse) => void;
  logout: () => void;
  isAuthenticated: boolean;
  userRole: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Check for existing token on app load
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const login = (tokenResponse: TokenResponse) => {
    console.log('🔐 AuthContext: Login called with:', tokenResponse);
    console.log('🔐 AuthContext: User role from backend:', tokenResponse.user.role);
    
    setToken(tokenResponse.access_token);
    setUser(tokenResponse.user);
    localStorage.setItem('access_token', tokenResponse.access_token);
    localStorage.setItem('user', JSON.stringify(tokenResponse.user));
    
    console.log('🔐 AuthContext: User state set, role:', tokenResponse.user.role);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  };

  const isAuthenticated = !!token && !!user;
  const userRole = user?.role || null;

  const value: AuthContextType = {
    user,
    token,
    login,
    logout,
    isAuthenticated,
    userRole,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 