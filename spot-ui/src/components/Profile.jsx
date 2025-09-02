import React, { useState, useEffect } from 'react';
import './Profile.css';

function Profile({ accessToken, onLogout }) {
  const [profile, setProfile] = useState(null);
  const [topArtists, setTopArtists] = useState([]);
  const [topTracks, setTopTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [selectedTrack, setSelectedTrack] = useState(null);

  // Function to close artist modal and clear any errors
  const closeArtistModal = () => {
    setSelectedArtist(null);
    setError(null);
  };

  // Function to close track modal and clear any errors
  const closeTrackModal = () => {
    setSelectedTrack(null);
    setError(null);
  };

  // Function to fetch detailed artist information
  const fetchArtistDetails = async (artistId) => {
    try {
      const response = await fetch(`http://localhost:4500/api/artist/${artistId}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (response.ok) {
        const artistData = await response.json();
        setSelectedArtist(artistData);
      } else {
        const errorData = await response.json();
        console.error('❌ Failed to fetch artist details:', response.status, errorData);
        setError(`Failed to fetch artist details: ${errorData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('💥 Error fetching artist details:', error);
      setError(`Network error: ${error.message}`);
    }
  };

  // Function to fetch detailed track information
  const fetchTrackDetails = async (trackId) => {
    try {
      const response = await fetch(`http://localhost:4500/api/song/${trackId}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        const trackData = await response.json();
        setSelectedTrack(trackData);
      } else {
        const errorData = await response.json();
        console.error('❌ Failed to fetch track details:', response.status, errorData);
        setError(`Failed to fetch track details: ${errorData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('💥 Error fetching track details:', error);
      setError(`Network error: ${error.message}`);
    }
  };

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        
        // Fetch profile data from Flask backend using new User model endpoint
        const profileResponse = await fetch('http://localhost:4500/api/user', {
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
            <div 
              key={index} 
              className="item clickable" 
              onClick={() => fetchArtistDetails(artist.id)}
              style={{ cursor: 'pointer' }}
            >
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
            <div 
              key={index} 
              className="item clickable" 
              onClick={() => fetchTrackDetails(track.id)}
              style={{ cursor: 'pointer' }}
            >
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

      {/* Artist Modal */}
      {selectedArtist && (
        <div className="modal-overlay" onClick={closeArtistModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🎤 Artist Details</h2>
              <button className="modal-close" onClick={closeArtistModal}>×</button>
            </div>
            <div className="modal-body">
              {selectedArtist.images && selectedArtist.images[0] && (
                <img 
                  src={selectedArtist.images[0].url} 
                  alt={selectedArtist.name}
                  className="modal-image"
                />
              )}
              <div className="modal-info">
                <h3>{selectedArtist.name}</h3>
                <p><strong>Genres:</strong> {selectedArtist.genres?.join(', ') || 'No genres listed'}</p>
                <p><strong>Popularity:</strong> {selectedArtist.popularity}/100</p>
                <p><strong>Followers:</strong> {selectedArtist.followers?.total?.toLocaleString() || 'Unknown'}</p>
                {selectedArtist.external_urls?.spotify && (
                  <a href={selectedArtist.external_urls.spotify} target="_blank" rel="noopener noreferrer" className="spotify-link">
                    Open in Spotify
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Track Modal */}
      {selectedTrack && (
        <div className="modal-overlay" onClick={closeTrackModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🎵 Track Details</h2>
              <button className="modal-close" onClick={closeTrackModal}>×</button>
            </div>
            <div className="modal-body">
              {selectedTrack.album?.images && selectedTrack.album.images[0] && (
                <img 
                  src={selectedTrack.album.images[0].url} 
                  alt={selectedTrack.album.name}
                  className="modal-image"
                />
              )}
              <div className="modal-info">
                <h3>{selectedTrack.name}</h3>
                <p><strong>Artists:</strong> {selectedTrack.artists?.map(artist => artist.name).join(', ')}</p>
                <p><strong>Album:</strong> {selectedTrack.album?.name}</p>
                <p><strong>Duration:</strong> {Math.floor(selectedTrack.duration_ms / 60000)}:{(selectedTrack.duration_ms % 60000 / 1000).toFixed(0).padStart(2, '0')}</p>
                <p><strong>Popularity:</strong> {selectedTrack.popularity}/100</p>
                <p><strong>Explicit:</strong> {selectedTrack.explicit ? 'Yes' : 'No'}</p>
                {selectedTrack.preview_url && (
                  <div className="audio-preview">
                    <p><strong>Preview:</strong></p>
                    <audio controls>
                      <source src={selectedTrack.preview_url} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                )}
                {selectedTrack.external_urls?.spotify && (
                  <a href={selectedTrack.external_urls.spotify} target="_blank" rel="noopener noreferrer" className="spotify-link">
                    Open in Spotify
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile; 