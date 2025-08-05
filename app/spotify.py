import requests
import os
from flask import session
from urllib.parse import quote
from http import HTTPStatus
from typing import Dict, Any, Optional
from app.spotify_exceptions import (
    SpotifyMissingConfigError,
    SpotifyTokenError,
    SpotifyAPIError,
    SpotifyInvalidResponseError
)

def get_auth_url() -> str:
    """Generate Spotify authorization URL"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    if not client_id or not redirect_uri:
        raise SpotifyMissingConfigError("Missing required environment variables: SPOTIFY_CLIENT_ID or SPOTIFY_REDIRECT_URI")
    
    if not redirect_uri.endswith('/callback'):
        raise SpotifyMissingConfigError("SPOTIFY_REDIRECT_URI must end with '/callback'. Current value: " + redirect_uri)
    
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={client_id}"
        "&response_type=code"
        f"&redirect_uri={quote(redirect_uri)}"
        "&scope=user-read-private%20user-read-email%20user-top-read"
    )
    
    return auth_url

def get_access_token(code: str) -> Dict[str, Any]:
    """Exchange authorization code for access token"""
    if not code:
        raise SpotifyTokenError("Authorization code is required")
    
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    if not redirect_uri:
        raise SpotifyMissingConfigError("Missing SPOTIFY_REDIRECT_URI environment variable")
    
    if not redirect_uri.endswith('/callback'):
        raise SpotifyMissingConfigError("SPOTIFY_REDIRECT_URI must end with '/callback'. Current value: " + redirect_uri)
        
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
    
    response_data = response.json()
    
    if response.status_code != HTTPStatus.OK:
        error_msg = response_data.get('error_description', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get access token: {error_msg}")
        
    return response_data

def get_profile(access_token: str) -> Dict[str, Any]:
    """Get user profile from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
        
    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    response_data = response.json()
    
    if response.status_code != HTTPStatus.OK:
        error_msg = response_data.get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get profile: {error_msg}")
        
    return response_data

def get_top_artists(access_token: str, time_range: str = 'medium_term', limit: int = 20) -> Dict[str, Any]:
    """Get user's top artists from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
    
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    response_data = response.json()
    
    if response.status_code != HTTPStatus.OK:
        error_msg = response_data.get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get top artists: {error_msg}")
    
    if not isinstance(response_data, dict) or 'items' not in response_data:
        raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top artists")
    
    return response_data

def get_top_tracks(access_token: str, time_range: str = 'medium_term', limit: int = 20) -> Dict[str, Any]:
    """Get user's top tracks from Spotify API"""
    if not access_token:
        raise SpotifyTokenError("Access token is required")
    
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    response_data = response.json()
    
    if response.status_code != HTTPStatus.OK:
        error_msg = response_data.get('error', {}).get('message', 'Unknown error')
        raise SpotifyAPIError(f"Failed to get top tracks: {error_msg}")
    
    if not isinstance(response_data, dict) or 'items' not in response_data:
        raise SpotifyInvalidResponseError("Invalid response format from Spotify API for top tracks")
    
    return response_data
