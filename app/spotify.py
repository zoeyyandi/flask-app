import requests
import os
import logging
from flask import session
from urllib.parse import quote
from app.spotify_exceptions import (
    SpotifyMissingConfigError,
    SpotifyTokenError,
    SpotifyAPIError,
    SpotifyInvalidResponseError
)

# Create logger for this module
logger = logging.getLogger(__name__)

def get_auth_url():
    """Generate Spotify authorization URL"""
    logger.info("Generating Spotify authorization URL")
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    if not client_id or not redirect_uri:
        logger.error("Missing required environment variables: SPOTIFY_CLIENT_ID or SPOTIFY_REDIRECT_URI")
        raise SpotifyMissingConfigError("Missing required environment variables: SPOTIFY_CLIENT_ID or SPOTIFY_REDIRECT_URI")
    
    logger.debug(f"Using client_id: {client_id[:10]}... and redirect_uri: {redirect_uri}")
    
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
    
    logger.info("Successfully generated Spotify authorization URL")
    return auth_url

def get_access_token(code):
    """Exchange authorization code for access token"""
    logger.info("Exchanging authorization code for access token")
    
    if not code:
        logger.error("Authorization code is missing")
        raise SpotifyTokenError("Authorization code is required")
    
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    if not redirect_uri.endswith('/callback'):
        redirect_uri = redirect_uri.rstrip('/') + '/callback'
    
    logger.debug("Making request to Spotify token endpoint")
    
    try:
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
        
        logger.debug(f"Token request response status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = response.json().get('error_description', 'Unknown error')
            logger.error(f"Failed to get access token. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get access token: {error_msg}")
        
        logger.info("Successfully obtained access token from Spotify")
        return response.json()
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting access token: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_profile(access_token):
    """Get user profile from Spotify API"""
    logger.info("Fetching user profile from Spotify API")
    
    if not access_token:
        logger.error("Access token is missing for profile request")
        raise SpotifyTokenError("Access token is required")
    
    logger.debug("Making request to Spotify profile endpoint")
    
    try:
        response = requests.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Profile request response status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get profile. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get profile: {error_msg}")
        
        profile_data = response.json()
        user_id = profile_data.get('id', 'unknown')
        logger.info(f"Successfully retrieved profile for user: {user_id}")
        return profile_data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting profile: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_top_artists(access_token, time_range='medium_term', limit=20):
    """Get user's top artists from Spotify API"""
    logger.info(f"Fetching top artists from Spotify API (time_range: {time_range}, limit: {limit})")
    
    if not access_token:
        logger.error("Access token is missing for top artists request")
        raise SpotifyTokenError("Access token is required")
    
    logger.debug("Making request to Spotify top artists endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Top artists request response status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get top artists. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get top artists: {error_msg}")
        
        data = response.json()
        
        if not isinstance(data, dict) or 'items' not in data:
            logger.error("Invalid response format from Spotify API for top artists")
            raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top artists")
        
        artist_count = len(data.get('items', []))
        logger.info(f"Successfully retrieved {artist_count} top artists")
        return data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting top artists: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_top_tracks(access_token, time_range='medium_term', limit=20):
    """Get user's top tracks from Spotify API"""
    logger.info(f"Fetching top tracks from Spotify API (time_range: {time_range}, limit: {limit})")
    
    if not access_token:
        logger.error("Access token is missing for top tracks request")
        raise SpotifyTokenError("Access token is required")
    
    logger.debug("Making request to Spotify top tracks endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Top tracks request response status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get top tracks. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get top tracks: {error_msg}")
        
        data = response.json()
        
        if not isinstance(data, dict) or 'items' not in data:
            logger.error("Invalid response format from Spotify API for top tracks")
            raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top tracks")
        
        track_count = len(data.get('items', []))
        logger.info(f"Successfully retrieved {track_count} top tracks")
        return data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting top tracks: {e}")
        raise SpotifyAPIError(f"Network error: {e}")
