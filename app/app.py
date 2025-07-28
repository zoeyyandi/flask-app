from flask import Flask, redirect, session, request, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.spotify import get_auth_url, get_access_token, get_profile, get_top_artists, get_top_tracks

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(get_auth_url())

@app.route('/callback')
def callback():
    token_data = get_access_token(request.args.get('code'))
    access_token = token_data['access_token']
    session['access_token'] = access_token
    
    # For React frontend, we'll redirect with the token as a query parameter
    # In production, you'd want to use a more secure method
    return redirect(f'http://localhost:5173/callback?token={access_token}')

@app.route('/profile')
def profile():
    if 'access_token' not in session:
        return render_template('profile.html', error="Not authenticated. Please log in first.")
    
    try:
        # Get user profile data
        profile_data = get_profile(session['access_token'])
        if not profile_data:
            raise Exception("Failed to get profile data")
        
        # Get user's top artists and top tracks
        top_artists_response = get_top_artists(session['access_token'])
        top_tracks_response = get_top_tracks(session['access_token'])

        # Render the profile template with all the data
        return render_template('profile.html', 
                             profile=profile_data, 
                             top_artists=top_artists_response.get('items', []), 
                             top_tracks=top_tracks_response.get('items', []))
    
    except Exception as e:
        print(f"Error in profile route: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return render_template('profile.html', error=f"Failed to get Spotify profile info: {str(e)}")

# API endpoints for React frontend
@app.route('/api/profile', methods=['GET'])
def api_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    
    try:
        profile_data = get_profile(access_token)
        if not profile_data:
            return jsonify({'error': 'Failed to get profile data'}), 500
        
        return jsonify(profile_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-artists', methods=['GET'])
def api_top_artists():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    
    try:
        top_artists_response = get_top_artists(access_token)
        return jsonify(top_artists_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-tracks', methods=['GET'])
def api_top_tracks():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    access_token = auth_header.split(' ')[1]
    
    try:
        top_tracks_response = get_top_tracks(access_token)
        return jsonify(top_tracks_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
