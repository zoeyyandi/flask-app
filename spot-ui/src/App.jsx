import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useSearchParams } from 'react-router-dom';
import Home from './components/Home';
import Profile from './components/Profile';
import Callback from './components/Callback';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    // Check if user is authenticated (you can store token in localStorage)
    const token = localStorage.getItem('spotify_access_token');
    if (token) {
      setAccessToken(token);
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    // Redirect to Flask backend login endpoint
    window.location.href = 'http://localhost:4500/login';
  };

  const handleLogout = () => {
    localStorage.removeItem('spotify_access_token');
    setAccessToken(null);
    setIsAuthenticated(false);
  };

  const handleAuthSuccess = (token) => {
    localStorage.setItem('spotify_access_token', token);
    setAccessToken(token);
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              <Home 
                onLogin={handleLogin}
                isAuthenticated={isAuthenticated}
              />
            } 
          />
          <Route 
            path="/callback" 
            element={
              <Callback onAuthSuccess={handleAuthSuccess} />
            } 
          />
          <Route 
            path="/profile" 
            element={
              isAuthenticated ? (
                <Profile 
                  accessToken={accessToken}
                  onLogout={handleLogout}
                />
              ) : (
                <Navigate to="/" replace />
              )
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 