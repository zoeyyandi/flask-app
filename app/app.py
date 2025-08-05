from flask import Flask, redirect, session, request, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from app.spotify import get_auth_url, get_access_token, get_profile, get_top_artists, get_top_tracks
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

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
