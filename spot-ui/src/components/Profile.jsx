import React, { useState, useEffect } from 'react';
import './Profile.css';

function Profile({ accessToken, onLogout }) {
  const [profile, setProfile] = useState(null);
  const [topArtists, setTopArtists] = useState([]);
  const [topTracks, setTopTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        
        // Fetch profile data from Flask backend
        const profileResponse = await fetch('http://localhost:4500/api/profile', {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        
        if (!profileResponse.ok) {
          throw new Error('Failed to fetch profile data');
        }
        
        const profileData = await profileResponse.json();
        setProfile(profileData);
        
        // Fetch top artists
        const artistsResponse = await fetch('http://localhost:4500/api/top-artists', {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        
        if (artistsResponse.ok) {
          const artistsData = await artistsResponse.json();
          setTopArtists(artistsData.items || []);
        }
        
        // Fetch top tracks
        const tracksResponse = await fetch('http://localhost:4500/api/top-tracks', {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        
        if (tracksResponse.ok) {
          const tracksData = await tracksResponse.json();
          setTopTracks(tracksData.items || []);
        }
        
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (accessToken) {
      fetchProfileData();
    }
  }, [accessToken]);

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading">Loading profile...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
        
        {profile?.images && (
          <img 
            src={profile.images[0].url} 
            alt="Profile Picture" 
            className="profile-image"
          />
        )}
        <div className="profile-info">
          <h1>{profile?.display_name}</h1>
          <p>Spotify User</p>
        </div>
      </div>
      
      <div className="profile-details">
        <div className="detail-item">
          <span className="detail-label">Email:</span>
          <span>{profile?.email}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Country:</span>
          <span>{profile?.country}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Product:</span>
          <span>{profile?.product}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Followers:</span>
          <span>{profile?.followers?.total}</span>
        </div>
      </div>

      <div className="top-items">
        <h2>Top Artists</h2>
        {topArtists.length > 0 ? (
          topArtists.map((artist, index) => (
            <div key={index} className="item">
              {artist.images && (
                <img 
                  src={artist.images[0].url} 
                  alt={artist.name}
                />
              )}
              <div className="item-info">
                <div className="item-name">{artist.name}</div>
                <div className="item-artist">
                  {artist.genres?.join(', ') || 'No genres listed'}
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No top artists found.</p>
        )}
      </div>

      <div className="top-items">
        <h2>Top Tracks</h2>
        {topTracks.length > 0 ? (
          topTracks.map((track, index) => (
            <div key={index} className="item">
              {track.album?.images && (
                <img 
                  src={track.album.images[0].url} 
                  alt={track.name}
                />
              )}
              <div className="item-info">
                <div className="item-name">{track.name}</div>
                <div className="item-artist">
                  {track.artists?.map(artist => artist.name).join(', ')}
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No top tracks found.</p>
        )}
      </div>
    </div>
  );
}

export default Profile; 