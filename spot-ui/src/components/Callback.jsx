import React, { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';

function Callback({ onAuthSuccess }) {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (token) {
      // Store the token and redirect to profile
      onAuthSuccess(token);
      navigate('/profile');
    } else {
      // No token found, redirect to home
      navigate('/');
    }
  }, [searchParams, onAuthSuccess, navigate]);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      backgroundColor: '#121212',
      color: 'white'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h2>Authenticating...</h2>
        <p>Please wait while we complete your login.</p>
      </div>
    </div>
  );
}

export default Callback; 