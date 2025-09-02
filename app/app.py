from flask import Flask, redirect, session, request, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from app.spotify import get_auth_url, get_access_token, get_profile, get_top_artists, get_top_tracks, get_artist, get_album, get_track, get_playlist
from app.models import User, Artist, Album, Song, Playlist
from app.spotify_exceptions import SpotifyError

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/login')
def login():
    logger.info("Login endpoint accessed - redirecting to Spotify auth")
    try:
        auth_url = get_auth_url()
        logger.info("Successfully generated Spotify auth URL")
        return redirect(auth_url)
    except SpotifyError as e:
        logger.error(f"Spotify error in login: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in login: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/callback')
def callback():
    code = request.args.get('code')
    logger.info(f"Callback endpoint accessed with code: {'present' if code else 'missing'}")
    
    try:
        token_data = get_access_token(code)
        access_token = token_data['access_token']
        session['access_token'] = access_token
        
        logger.info("Successfully obtained access token and stored in session")
        
        # For React frontend, we'll redirect with the token as a query parameter
        # In production, you'd want to use a more secure method
        redirect_url = f'http://localhost:5173/callback?token={access_token}'
        logger.info("Redirecting to React frontend with token")
        return redirect(redirect_url)
        
    except SpotifyError as e:
        logger.error(f"Spotify error in callback: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in callback: {e}")
        return jsonify({'error': 'Failed to process callback'}), 500

@app.route('/profile')
def profile():
    logger.info("Profile page accessed")
    
    if 'access_token' not in session:
        logger.warning("Profile access attempted without authentication")
        return render_template('profile.html', error="Not authenticated. Please log in first.")
    
    try:
        logger.info("Fetching user profile data from Spotify")
        # Get user profile data
        profile_data = get_profile(session['access_token'])
        if not profile_data:
            logger.error("Profile data is empty")
            raise Exception("Failed to get profile data")
        
        logger.info("Successfully retrieved profile data")
        
        # Get user's top artists and top tracks
        logger.info("Fetching user's top artists and tracks")
        top_artists_response = get_top_artists(session['access_token'])
        top_tracks_response = get_top_tracks(session['access_token'])
        
        logger.info("Successfully retrieved top artists and tracks")

        # Render the profile template with all the data
        return render_template('profile.html', 
                             profile=profile_data, 
                             top_artists=top_artists_response.get('items', []), 
                             top_tracks=top_tracks_response.get('items', []))
    
    except SpotifyError as e:
        logger.error(f"Spotify error in profile route: {e}")
        return render_template('profile.html', error=f"Spotify error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in profile route: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        return render_template('profile.html', error=f"Failed to get Spotify profile info: {str(e)}")

# API endpoints for React frontend
@app.route('/api/profile', methods=['GET'])
def api_profile():
    logger.info("API profile endpoint accessed")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API profile access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API profile")
    
    try:
        logger.info("Fetching profile data via API")
        profile_data = get_profile(access_token)
        if not profile_data:
            logger.error("Profile data is empty in API call")
            return jsonify({'error': 'Failed to get profile data'}), 500
        
        logger.info("Successfully retrieved profile data via API")
        return jsonify(profile_data)
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API profile: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API profile: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/top-artists', methods=['GET'])
def api_top_artists():
    logger.info("API top artists endpoint accessed")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API top artists access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API top artists")
    
    try:
        logger.info("Fetching top artists data via API")
        top_artists_response = get_top_artists(access_token)
        logger.info("Successfully retrieved top artists data via API")
        return jsonify(top_artists_response)
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API top artists: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API top artists: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/top-tracks', methods=['GET'])
def api_top_tracks():
    logger.info("API top tracks endpoint accessed")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API top tracks access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API top tracks")
    
    try:
        logger.info("Fetching top tracks data via API")
        top_tracks_response = get_top_tracks(access_token)
        logger.info("Successfully retrieved top tracks data via API")
        return jsonify(top_tracks_response)
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API top tracks: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API top tracks: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Individual object endpoints
@app.route('/api/user', methods=['GET'])
def api_user():
    """Get current user profile as User model object"""
    logger.info("API user endpoint accessed")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API user access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API user")
    
    try:
        logger.info("Fetching user profile data via API")
        profile_data = get_profile(access_token)
        if not profile_data:
            logger.error("Profile data is empty in API call")
            return jsonify({'error': 'Failed to get profile data'}), 500
        
        # Convert to User model
        user = User(
            id=profile_data.get('id'),
            display_name=profile_data.get('display_name'),
            email=profile_data.get('email'),
            country=profile_data.get('country'),
            product=profile_data.get('product'),
            followers=profile_data.get('followers'),
            images=profile_data.get('images'),
            external_urls=profile_data.get('external_urls'),
            href=profile_data.get('href'),
            uri=profile_data.get('uri')
        )
        
        logger.info("Successfully retrieved and converted user profile data via API")
        return jsonify(user.to_json()), 200
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API user: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API user: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/artist/<artist_id>', methods=['GET'])
def api_artist(artist_id):
    """Get specific artist as Artist model object"""
    logger.info(f"API artist endpoint accessed for artist: {artist_id}")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API artist access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API artist")
    
    try:
        logger.info(f"Fetching artist {artist_id} data via API")
        artist_data = get_artist(access_token, artist_id)
        if not artist_data:
            logger.error("Artist data is empty in API call")
            return jsonify({'error': 'Failed to get artist data'}), 500
        
        # Convert to Artist model
        artist = Artist(
            id=artist_data.get('id'),
            name=artist_data.get('name'),
            genres=artist_data.get('genres'),
            popularity=artist_data.get('popularity'),
            images=artist_data.get('images'),
            external_urls=artist_data.get('external_urls'),
            href=artist_data.get('href'),
            uri=artist_data.get('uri'),
            followers=artist_data.get('followers')
        )
        
        logger.info(f"Successfully retrieved and converted artist {artist_id} data via API")
        return jsonify(artist.to_json()), 200
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API artist: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API artist: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/album/<album_id>', methods=['GET'])
def api_album(album_id):
    """Get specific album as Album model object"""
    logger.info(f"API album endpoint accessed for album: {album_id}")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API album access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API album")
    
    try:
        logger.info(f"Fetching album {album_id} data via API")
        album_data = get_album(access_token, album_id)
        if not album_data:
            logger.error("Album data is empty in API call")
            return jsonify({'error': 'Failed to get album data'}), 500
        
        # Convert to Album model
        album = Album(
            id=album_data.get('id'),
            name=album_data.get('name'),
            album_type=album_data.get('album_type'),
            artists=album_data.get('artists'),
            available_markets=album_data.get('available_markets'),
            external_urls=album_data.get('external_urls'),
            href=album_data.get('href'),
            images=album_data.get('images'),
            release_date=album_data.get('release_date'),
            release_date_precision=album_data.get('release_date_precision'),
            total_tracks=album_data.get('total_tracks'),
            uri=album_data.get('uri'),
            genres=album_data.get('genres'),
            label=album_data.get('label'),
            popularity=album_data.get('popularity')
        )
        
        logger.info(f"Successfully retrieved and converted album {album_id} data via API")
        return jsonify(album.to_json()), 200
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API album: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API album: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/song/<track_id>', methods=['GET'])
def api_song(track_id):
    """Get specific track as Song model object"""
    logger.info(f"API song endpoint accessed for track: {track_id}")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API song access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API song")
    
    try:
        logger.info(f"Fetching track {track_id} data via API")
        track_data = get_track(access_token, track_id)
        if not track_data:
            logger.error("Track data is empty in API call")
            return jsonify({'error': 'Failed to get track data'}), 500
        
        # Convert to Song model
        song = Song(
            id=track_data.get('id'),
            name=track_data.get('name'),
            album=track_data.get('album'),
            artists=track_data.get('artists'),
            available_markets=track_data.get('available_markets'),
            disc_number=track_data.get('disc_number'),
            duration_ms=track_data.get('duration_ms'),
            explicit=track_data.get('explicit'),
            external_urls=track_data.get('external_urls'),
            href=track_data.get('href'),
            is_local=track_data.get('is_local'),
            popularity=track_data.get('popularity'),
            preview_url=track_data.get('preview_url'),
            track_number=track_data.get('track_number'),
            uri=track_data.get('uri')
        )
        
        logger.info(f"Successfully retrieved and converted track {track_id} data via API")
        return jsonify(song.to_json()), 200
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API song: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API song: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/playlist/<playlist_id>', methods=['GET'])
def api_playlist(playlist_id):
    """Get specific playlist as Playlist model object"""
    logger.info(f"API playlist endpoint accessed for playlist: {playlist_id}")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("API playlist access attempted with missing or invalid authorization header")
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    logger.info("Valid authorization header provided for API playlist")
    
    try:
        logger.info(f"Fetching playlist {playlist_id} data via API")
        playlist_data = get_playlist(access_token, playlist_id)
        if not playlist_data:
            logger.error("Playlist data is empty in API call")
            return jsonify({'error': 'Failed to get playlist data'}), 500
        
        # Convert to Playlist model
        playlist = Playlist(
            id=playlist_data.get('id'),
            name=playlist_data.get('name'),
            description=playlist_data.get('description'),
            owner=playlist_data.get('owner'),
            public=playlist_data.get('public'),
            collaborative=playlist_data.get('collaborative'),
            external_urls=playlist_data.get('external_urls'),
            href=playlist_data.get('href'),
            images=playlist_data.get('images'),
            snapshot_id=playlist_data.get('snapshot_id'),
            tracks=playlist_data.get('tracks'),
            uri=playlist_data.get('uri'),
            followers=playlist_data.get('followers')
        )
        
        logger.info(f"Successfully retrieved and converted playlist {playlist_id} data via API")
        return jsonify(playlist.to_json()), 200
        
    except SpotifyError as e:
        logger.error(f"Spotify error in API playlist: {e}")
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in API playlist: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
