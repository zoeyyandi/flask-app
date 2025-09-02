from app.exceptions import ClientError
from werkzeug.exceptions import (
    InternalServerError,
    Unauthorized,
    BadRequest,
    NotFound
)

class SpotifyError(ClientError):
    """Base class for Spotify-related errors"""
    status_code = InternalServerError.code
    message = "SPOTIFY_ERROR"

class SpotifyAuthError(SpotifyError):
    """Errors related to Spotify authentication"""
    status_code = Unauthorized.code
    message = "SPOTIFY_AUTHENTICATION_ERROR"

class SpotifyTokenError(SpotifyAuthError):
    """Errors related to access token"""
    status_code = Unauthorized.code
    message = "SPOTIFY_TOKEN_ERROR"

class SpotifyAPIError(SpotifyError):
    """Errors from Spotify API responses"""
    status_code = BadRequest.code
    message = "SPOTIFY_API_ERROR"
    
    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code

class SpotifyInvalidResponseError(SpotifyError):
    """Errors related to invalid response format"""
    status_code = InternalServerError.code
    message = "SPOTIFY_INVALID_RESPONSE_ERROR"

class SpotifyMissingConfigError(SpotifyError):
    """Errors related to missing configuration"""
    status_code = InternalServerError.code
    message = "SPOTIFY_MISSING_CONFIG_ERROR" 