import React from 'react';
import './Home.css';

function Home({ onLogin, isAuthenticated }) {
  return (
    <div className="home">
      <div className="container">
        <img 
          src="https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png" 
          alt="Spotify Logo" 
          className="logo"
        />
        <h1>Welcome to Spot</h1>
        <p>View your Spotify profile information and connect with your music world</p>
        
        {!isAuthenticated ? (
          <button onClick={onLogin} className="login-button">
            Login with Spotify
          </button>
        ) : (
          <div className="authenticated-actions">
            <p>You're logged in!</p>
            <a href="/profile" className="profile-button">
              View Profile
            </a>
          </div>
        )}
        
        <div className="features">
          <div className="feature">
            <h3>Profile Info</h3>
            <p>View your display name, email, and account details</p>
          </div>
          <div className="feature">
            <h3>Followers</h3>
            <p>See how many followers you have on Spotify</p>
          </div>
          <div className="feature">
            <h3>Account Type</h3>
            <p>Check your Spotify subscription status</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home; 