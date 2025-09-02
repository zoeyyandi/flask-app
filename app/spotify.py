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

def get_artist(access_token, artist_id):
    """Get a specific artist from Spotify API"""
    logger.info(f"Fetching artist {artist_id} from Spotify API")
    
    if not access_token:
        logger.error("Access token is missing for artist request")
        raise SpotifyTokenError("Access token is required")
    
    if not artist_id:
        logger.error("Artist ID is missing")
        raise SpotifyAPIError("Artist ID is required")
    
    logger.debug("Making request to Spotify artist endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Artist request response status: {response.status_code}")
        
        if response.status_code == 404:
            logger.warning(f"Artist {artist_id} not found")
            raise SpotifyAPIError("Artist not found", status_code=404)
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get artist. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get artist: {error_msg}")
        
        artist_data = response.json()
        logger.info(f"Successfully retrieved artist: {artist_data.get('name', 'Unknown')}")
        return artist_data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting artist: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_album(access_token, album_id):
    """Get a specific album from Spotify API"""
    logger.info(f"Fetching album {album_id} from Spotify API")
    
    if not access_token:
        logger.error("Access token is missing for album request")
        raise SpotifyTokenError("Access token is required")
    
    if not album_id:
        logger.error("Album ID is missing")
        raise SpotifyAPIError("Album ID is required")
    
    logger.debug("Making request to Spotify album endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/albums/{album_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Album request response status: {response.status_code}")
        
        if response.status_code == 404:
            logger.warning(f"Album {album_id} not found")
            raise SpotifyAPIError("Album not found", status_code=404)
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get album. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get album: {error_msg}")
        
        album_data = response.json()
        logger.info(f"Successfully retrieved album: {album_data.get('name', 'Unknown')}")
        return album_data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting album: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_track(access_token, track_id):
    """Get a specific track from Spotify API"""
    logger.info(f"Fetching track {track_id} from Spotify API")
    
    if not access_token:
        logger.error("Access token is missing for track request")
        raise SpotifyTokenError("Access token is required")
    
    if not track_id:
        logger.error("Track ID is missing")
        raise SpotifyAPIError("Track ID is required")
    
    logger.debug("Making request to Spotify track endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{track_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Track request response status: {response.status_code}")
        
        if response.status_code == 404:
            logger.warning(f"Track {track_id} not found")
            raise SpotifyAPIError("Track not found", status_code=404)
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get track. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get track: {error_msg}")
        
        track_data = response.json()
        logger.info(f"Successfully retrieved track: {track_data.get('name', 'Unknown')}")
        return track_data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting track: {e}")
        raise SpotifyAPIError(f"Network error: {e}")

def get_playlist(access_token, playlist_id):
    """Get a specific playlist from Spotify API"""
    logger.info(f"Fetching playlist {playlist_id} from Spotify API")
    
    if not access_token:
        logger.error("Access token is missing for playlist request")
        raise SpotifyTokenError("Access token is required")
    
    if not playlist_id:
        logger.error("Playlist ID is missing")
        raise SpotifyAPIError("Playlist ID is required")
    
    logger.debug("Making request to Spotify playlist endpoint")
    
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        logger.debug(f"Playlist request response status: {response.status_code}")
        
        if response.status_code == 404:
            logger.warning(f"Playlist {playlist_id} not found")
            raise SpotifyAPIError("Playlist not found", status_code=404)
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Failed to get playlist. Status: {response.status_code}, Error: {error_msg}")
            raise SpotifyAPIError(f"Failed to get playlist: {error_msg}")
        
        playlist_data = response.json()
        logger.info(f"Successfully retrieved playlist: {playlist_data.get('name', 'Unknown')}")
        return playlist_data
        
    except requests.RequestException as e:
        logger.error(f"Network error while requesting playlist: {e}")
        raise SpotifyAPIError(f"Network error: {e}")
