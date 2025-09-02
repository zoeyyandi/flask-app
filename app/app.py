from flask import Flask, redirect, session, request, render_template
from dotenv import load_dotenv
import os
import traceback
from app.spotify import get_auth_url, get_access_token, get_profile, get_top_artists, get_top_tracks

load_dotenv()

app = Flask(__name__)
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
    session['access_token'] = token_data['access_token']
    return redirect('/profile')

@app.route('/profile')
def profile():
    if 'access_token' not in session:
        return render_template('profile.html', error='Not authenticated. Please log in first.')
    
    try:
        # Get user profile data
        profile_data = get_profile(session['access_token'])
        if not profile_data:
            raise Exception('Failed to get profile data')
        
        # Get user's top artists and top tracks
        top_artists_response = get_top_artists(session['access_token'])
        top_tracks_response = get_top_tracks(session['access_token'])

        # Render the profile template with all the data
        return render_template('profile.html', 
                             profile=profile_data, 
                             top_artists=top_artists_response.get('items', []), 
                             top_tracks=top_tracks_response.get('items', []))
    
    except Exception as e:
        print(f'Error in profile route: {str(e)}')
        print(f'Error type: {type(e)}')
        print(f'Traceback: {traceback.format_exc()}')
        return render_template('profile.html', error=f'Failed to get Spotify profile info: {str(e)}')
