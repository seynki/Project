import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored authentication on component mount
    const token = localStorage.getItem('auth_token');
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');

    if (token && userId && username) {
      setUser({
        id: userId,
        username: username,
        token: token
      });
    }
    setIsLoading(false);
  }, []);

  const login = (userData) => {
    setUser({
      id: userData.user_id,
      username: userData.username,
      token: userData.access_token
    });
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;