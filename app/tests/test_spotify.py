import pytest
from app.spotify import get_auth_url, get_access_token, get_profile, get_top_artists, get_top_tracks
from app.spotify_exceptions import (
    SpotifyMissingConfigError,
    SpotifyTokenError,
    SpotifyAPIError,
    SpotifyInvalidResponseError
)
import os
from dotenv import load_dotenv
from urllib.parse import quote
import responses

# Load environment variables for testing
load_dotenv()

# Fixtures
@pytest.fixture
def mock_access_token_response():
    return {
        "access_token": "mock_access_token",
        "token_type": "Bearer",
        "expires_in": 3600
    }

@pytest.fixture
def mock_profile_response():
    return {
        "id": "mock_user_id",
        "display_name": "Test User",
        "email": "test@example.com",
        "images": [{"url": "https://example.com/image.jpg"}]
    }

@pytest.fixture
def mock_top_artists_response():
    return {
        "items": [
            {
                "id": "artist1",
                "name": "Artist One",
                "images": [{"url": "https://example.com/artist1.jpg"}],
                "genres": ["rock", "indie"]
            },
            {
                "id": "artist2",
                "name": "Artist Two",
                "images": [{"url": "https://example.com/artist2.jpg"}],
                "genres": ["pop", "electronic"]
            }
        ]
    }

@pytest.fixture
def mock_top_tracks_response():
    return {
        "items": [
            {
                "id": "track1",
                "name": "Track One",
                "artists": [{"name": "Artist One"}],
                "album": {
                    "name": "Album One",
                    "images": [{"url": "https://example.com/album1.jpg"}]
                }
            },
            {
                "id": "track2",
                "name": "Track Two",
                "artists": [{"name": "Artist Two"}],
                "album": {
                    "name": "Album Two",
                    "images": [{"url": "https://example.com/album2.jpg"}]
                }
            }
        ]
    }

# Test cases
def test_get_auth_url():
    """Test that auth URL is generated correctly"""
    auth_url = get_auth_url()
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    # Check that URL contains required components
    assert "https://accounts.spotify.com/authorize" in auth_url
    assert "client_id=" in auth_url
    assert "response_type=code" in auth_url
    assert "redirect_uri=" in auth_url
    assert "scope=user-read-private%20user-read-email%20user-top-read" in auth_url
    
    # Check that environment variables are properly inserted
    assert os.getenv('SPOTIFY_CLIENT_ID') in auth_url
    assert quote(redirect_uri) in auth_url

@responses.activate
def test_get_access_token_success(mock_access_token_response):
    """Test successful access token request"""
    responses.add(
        responses.POST,
        "https://accounts.spotify.com/api/token",
        json=mock_access_token_response,
        status=200
    )
    
    result = get_access_token("valid_code")
    assert result == mock_access_token_response
    assert result["access_token"] == "mock_access_token"

@responses.activate
def test_get_profile_success(mock_profile_response):
    """Test successful profile request"""
    responses.add(
        responses.GET,
        "https://api.spotify.com/v1/me",
        json=mock_profile_response,
        status=200
    )
    
    result = get_profile("valid_token")
    assert result == mock_profile_response
    assert result["display_name"] == "Test User"

@responses.activate
def test_get_top_artists_success(mock_top_artists_response):
    """Test successful top artists request"""
    responses.add(
        responses.GET,
        "https://api.spotify.com/v1/me/top/artists",
        json=mock_top_artists_response,
        status=200
    )
    
    result = get_top_artists("valid_token")
    assert result == mock_top_artists_response
    assert len(result["items"]) == 2
    assert result["items"][0]["name"] == "Artist One"
    assert result["items"][1]["name"] == "Artist Two"

@responses.activate
def test_get_top_tracks_success(mock_top_tracks_response):
    """Test successful top tracks request"""
    responses.add(
        responses.GET,
        "https://api.spotify.com/v1/me/top/tracks",
        json=mock_top_tracks_response,
        status=200
    )
    
    result = get_top_tracks("valid_token")
    assert result == mock_top_tracks_response
    assert len(result["items"]) == 2
    assert result["items"][0]["name"] == "Track One"
    assert result["items"][1]["name"] == "Track Two"

# Parametrized tests for error cases
@pytest.mark.parametrize("function,args,expected_exception", [
    (get_access_token, ["invalid_code"], SpotifyAPIError),  # Most common auth error
    (get_profile, ["invalid_token"], SpotifyAPIError),      # Most common API error
    (get_top_artists, [None], SpotifyTokenError),          # Missing token validation
])
def test_error_cases(function, args, expected_exception):
    """Test various error cases for all functions"""
    with pytest.raises(expected_exception):
        function(*args) 