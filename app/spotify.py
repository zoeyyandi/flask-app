import requests
import os
from flask import session
from urllib.parse import quote
from app.spotify_exceptions import (
    SpotifyMissingConfigError,
    SpotifyTokenError,
    SpotifyAPIError,
    SpotifyInvalidResponseError
)

def get_auth_url():
    """Generate Spotify authorization URL"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    if not client_id or not redirect_uri:
        raise SpotifyMissingConfigError("Missing required environment variables: SPOTIFY_CLIENT_ID or SPOTIFY_REDIRECT_URI")
    
    # Ensure redirect URI ends with /callback
    if not redirect_uri.endswith('/callback'):
        redirect_uri = redirect_uri.rstrip('/') + '/callback'
    
    # Remove any trailing slashes except after /callback
    redirect_uri = redirect_uri.rstrip('/')
    if not redirect_uri.endswith('/callback'):
        redirect_uri += '/callback'
    
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={client_id}"
        "&response_type=code"
        f"&redirect_uri={quote(redirect_uri)}"
        "&scope=user-read-private%20user-read-email%20user-top-read"
    )
    
    return auth_url

def get_access_token(code):
    """Exchange authorization code for access token"""
    if not code:
        raise SpotifyTokenError("Authorization code is required")
    
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    if not redirect_uri.endswith('/callback'):
        redirect_uri = redirect_uri.rstrip('/') + '/callback'
        
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
            "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
        }
    )
    
    if response.status_code != 200:
        error_msg = response.json().get('error_description', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get access token: {error_msg}")
        
    return response.json()

def get_profile(access_token):
    """Get user profile from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
        
    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get profile: {error_msg}")
        
    return response.json()

def get_top_artists(access_token, time_range='medium_term', limit=20):
    """Get user's top artists from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
    
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get top artists: {error_msg}")
    
    data = response.json()
    
    if not isinstance(data, dict) or 'items' not in data:
        raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top artists")
    
    return data

def get_top_tracks(access_token, time_range='medium_term', limit=20):
    """Get user's top tracks from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
    
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get top tracks: {error_msg}")
    
    data = response.json()
    
    if not isinstance(data, dict) or 'items' not in data:
        raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top tracks")
    
    return data
