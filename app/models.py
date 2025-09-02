"""
Data models for the Spotify Insights Dashboard.

This module contains class definitions for User, Song, Album, Playlist, and Artist objects
that represent the core entities in the Spotify ecosystem.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime


class User:
    """Represents a Spotify user with profile information and listening data."""
    
    def __init__(self, 
                 id: str,
                 display_name: Optional[str] = None,
                 email: Optional[str] = None,
                 country: Optional[str] = None,
                 product: Optional[str] = None,
                 followers: Optional[Dict[str, int]] = None,
                 images: Optional[List[Dict[str, Any]]] = None,
                 external_urls: Optional[Dict[str, str]] = None,
                 href: Optional[str] = None,
                 uri: Optional[str] = None,
                 # Custom fields for app functionality
                 created_at: Optional[datetime] = None):
        """
        Initialize a User object.
        
        Args:
            id: Unique Spotify user identifier (matches Spotify API 'id' field)
            display_name: User's display name (can be None if not set by user)
            email: User's email address (requires user-read-email scope)
            country: User's country code (requires user-read-private scope)
            product: Spotify subscription type (free, premium, etc.)
            followers: Dictionary with 'total' key containing follower count
            images: List of profile images
            external_urls: External URLs for the user
            href: Spotify API href for the user
            uri: Spotify URI for the user
            created_at: When the user object was created (custom field)
        """
        self.id = id
        self.display_name = display_name
        self.email = email
        self.country = country
        self.product = product
        self.followers = followers or {"total": 0}
        self.images = images or []
        self.external_urls = external_urls or {}
        self.href = href
        self.uri = uri
        # Custom field for app functionality
        self.created_at = created_at or datetime.now()
    
    def to_json(self) -> Dict[str, Any]:
        """Convert User object to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'display_name': self.display_name,
            'email': self.email,
            'country': self.country,
            'product': self.product,
            'followers': self.followers,
            'images': self.images,
            'external_urls': self.external_urls,
            'href': self.href,
            'uri': self.uri,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Artist:
    """Represents a musical artist with metadata and popularity information."""
    
    def __init__(self,
                 id: str,
                 name: str,
                 genres: Optional[List[str]] = None,
                 popularity: Optional[int] = None,
                 images: Optional[List[Dict[str, Any]]] = None,
                 external_urls: Optional[Dict[str, str]] = None,
                 href: Optional[str] = None,
                 uri: Optional[str] = None,
                 followers: Optional[Dict[str, int]] = None,
                 # Custom fields for app functionality
                 created_at: Optional[datetime] = None):
        """
        Initialize an Artist object.
        
        Args:
            id: Unique Spotify artist identifier (matches Spotify API 'id' field)
            name: Artist name
            genres: List of genres associated with the artist
            popularity: Popularity score (0-100)
            images: List of artist images
            external_urls: External URLs for the artist
            href: Spotify API href for the artist
            uri: Spotify URI for the artist
            followers: Dictionary with 'total' key containing follower count
            created_at: When the artist object was created (custom field)
        """
        self.id = id
        self.name = name
        self.genres = genres or []
        self.popularity = popularity or 0
        self.images = images or []
        self.external_urls = external_urls or {}
        self.href = href
        self.uri = uri
        self.followers = followers or {"total": 0}
        # Custom field for app functionality
        self.created_at = created_at or datetime.now()
    
    def to_json(self) -> Dict[str, Any]:
        """Convert Artist object to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'popularity': self.popularity,
            'images': self.images,
            'external_urls': self.external_urls,
            'href': self.href,
            'uri': self.uri,
            'followers': self.followers,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Album:
    """Represents a music album with metadata and track information."""
    
    def __init__(self,
                 id: str,
                 name: str,
                 album_type: str,
                 artists: Optional[List[Dict[str, Any]]] = None,
                 available_markets: Optional[List[str]] = None,
                 external_urls: Optional[Dict[str, str]] = None,
                 href: Optional[str] = None,
                 images: Optional[List[Dict[str, Any]]] = None,
                 release_date: Optional[str] = None,
                 release_date_precision: Optional[str] = None,
                 total_tracks: Optional[int] = None,
                 uri: Optional[str] = None,
                 # Additional Spotify API fields
                 genres: Optional[List[str]] = None,
                 label: Optional[str] = None,
                 popularity: Optional[int] = None,
                 # Custom fields for app functionality
                 created_at: Optional[datetime] = None):
        """
        Initialize an Album object.
        
        Args:
            id: Unique Spotify album identifier (matches Spotify API 'id' field)
            name: Album name
            album_type: Type of album (album, single, compilation)
            artists: List of artists on the album
            available_markets: Markets where album is available
            external_urls: External URLs for the album
            href: Spotify API href for the album
            images: List of album cover images
            release_date: Album release date
            release_date_precision: Precision of release date
            total_tracks: Total number of tracks
            uri: Spotify URI for the album
            genres: List of genres associated with the album
            label: Label associated with the album
            popularity: Popularity score (0-100)
            created_at: When the album object was created (custom field)
        """
        self.id = id
        self.name = name
        self.album_type = album_type
        self.artists = artists or []
        self.available_markets = available_markets or []
        self.external_urls = external_urls or {}
        self.href = href
        self.images = images or []
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks or 0
        self.uri = uri
        self.genres = genres or []
        self.label = label
        self.popularity = popularity or 0
        # Custom field for app functionality
        self.created_at = created_at or datetime.now()
    
    def to_json(self) -> Dict[str, Any]:
        """Convert Album object to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'album_type': self.album_type,
            'artists': self.artists,
            'available_markets': self.available_markets,
            'external_urls': self.external_urls,
            'href': self.href,
            'images': self.images,
            'release_date': self.release_date,
            'release_date_precision': self.release_date_precision,
            'total_tracks': self.total_tracks,
            'uri': self.uri,
            'genres': self.genres,
            'label': self.label,
            'popularity': self.popularity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Song:
    """Represents a musical track with audio features and metadata."""
    
    def __init__(self,
                 id: str,
                 name: str,
                 album: Optional[Dict[str, Any]] = None,
                 artists: Optional[List[Dict[str, Any]]] = None,
                 available_markets: Optional[List[str]] = None,
                 disc_number: Optional[int] = None,
                 duration_ms: Optional[int] = None,
                 explicit: Optional[bool] = None,
                 external_urls: Optional[Dict[str, str]] = None,
                 href: Optional[str] = None,
                 is_local: Optional[bool] = None,
                 popularity: Optional[int] = None,
                 preview_url: Optional[str] = None,
                 track_number: Optional[int] = None,
                 uri: Optional[str] = None,
                 # Audio features for Music DNA analysis (from separate API endpoint)
                 danceability: Optional[float] = None,
                 energy: Optional[float] = None,
                 key: Optional[int] = None,
                 loudness: Optional[float] = None,
                 mode: Optional[int] = None,
                 speechiness: Optional[float] = None,
                 acousticness: Optional[float] = None,
                 instrumentalness: Optional[float] = None,
                 liveness: Optional[float] = None,
                 valence: Optional[float] = None,
                 tempo: Optional[float] = None,
                 time_signature: Optional[int] = None,
                 # Custom fields for app functionality
                 last_played: Optional[datetime] = None,
                 play_count: Optional[int] = None,
                 created_at: Optional[datetime] = None):
        """
        Initialize a Song object.
        
        Args:
            id: Unique Spotify track identifier (matches Spotify API 'id' field)
            name: Track name
            album: Album information
            artists: List of artists on the track
            available_markets: Markets where track is available
            disc_number: Disc number in album
            duration_ms: Track duration in milliseconds
            explicit: Whether track contains explicit content
            external_urls: External URLs for the track
            href: Spotify API href for the track
            is_local: Whether track is local file
            popularity: Popularity score (0-100)
            preview_url: URL for 30-second preview
            track_number: Track number in album
            uri: Spotify URI for the track
            # Audio features (from separate Spotify Audio Features API endpoint)
            danceability: How suitable for dancing (0.0-1.0)
            energy: Perceptual measure of intensity (0.0-1.0)
            key: Key the track is in (0-11)
            loudness: Overall loudness in dB
            mode: Major (1) or minor (0)
            speechiness: Presence of spoken words (0.0-1.0)
            acousticness: Confidence measure of acousticness (0.0-1.0)
            instrumentalness: Predicts if track contains vocals (0.0-1.0)
            liveness: Detects presence of audience (0.0-1.0)
            valence: Musical positivity (0.0-1.0)
            tempo: Overall estimated tempo in BPM
            time_signature: Estimated time signature
            # Custom fields for app functionality
            last_played: When track was last played
            play_count: Number of times played
            created_at: When the song object was created
        """
        self.id = id
        self.name = name
        self.album = album or {}
        self.artists = artists or []
        self.available_markets = available_markets or []
        self.disc_number = disc_number
        self.duration_ms = duration_ms or 0
        self.explicit = explicit or False
        self.external_urls = external_urls or {}
        self.href = href
        self.is_local = is_local or False
        self.popularity = popularity or 0
        self.preview_url = preview_url
        self.track_number = track_number
        self.uri = uri
        
        # Audio features
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.time_signature = time_signature
        
        # Custom fields for app functionality
        self.last_played = last_played
        self.play_count = play_count or 0
        self.created_at = created_at or datetime.now()
    
    def to_json(self) -> Dict[str, Any]:
        """Convert Song object to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'album': self.album,
            'artists': self.artists,
            'available_markets': self.available_markets,
            'disc_number': self.disc_number,
            'duration_ms': self.duration_ms,
            'explicit': self.explicit,
            'external_urls': self.external_urls,
            'href': self.href,
            'is_local': self.is_local,
            'popularity': self.popularity,
            'preview_url': self.preview_url,
            'track_number': self.track_number,
            'uri': self.uri,
            # Audio features
            'danceability': self.danceability,
            'energy': self.energy,
            'key': self.key,
            'loudness': self.loudness,
            'mode': self.mode,
            'speechiness': self.speechiness,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'liveness': self.liveness,
            'valence': self.valence,
            'tempo': self.tempo,
            'time_signature': self.time_signature,
            # Playback data
            'last_played': self.last_played.isoformat() if self.last_played else None,
            'play_count': self.play_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Playlist:
    """Represents a Spotify playlist with tracks and metadata."""
    
    def __init__(self,
                 id: str,
                 name: str,
                 description: Optional[str] = None,
                 owner: Optional[Dict[str, Any]] = None,
                 public: Optional[bool] = None,
                 collaborative: Optional[bool] = None,
                 external_urls: Optional[Dict[str, str]] = None,
                 href: Optional[str] = None,
                 images: Optional[List[Dict[str, Any]]] = None,
                 snapshot_id: Optional[str] = None,
                 tracks: Optional[Dict[str, Any]] = None,
                 uri: Optional[str] = None,
                 # Additional Spotify API fields
                 followers: Optional[Dict[str, int]] = None,
                 # Custom fields for AI Playlist Doctor features
                 analysis_score: Optional[float] = None,
                 tempo_consistency: Optional[float] = None,
                 key_consistency: Optional[float] = None,
                 energy_flow: Optional[float] = None,
                 genre_diversity: Optional[float] = None,
                 recommendations: Optional[List[str]] = None,
                 created_at: Optional[datetime] = None):
        """
        Initialize a Playlist object.
        
        Args:
            id: Unique Spotify playlist identifier (matches Spotify API 'id' field)
            name: Playlist name
            description: Playlist description
            owner: Playlist owner information
            public: Whether playlist is public
            collaborative: Whether playlist is collaborative
            external_urls: External URLs for the playlist
            href: Spotify API href for the playlist
            images: List of playlist cover images
            snapshot_id: Current snapshot ID
            tracks: Dictionary containing track information (includes 'total' count)
            uri: Spotify URI for the playlist
            followers: Dictionary with 'total' key containing follower count
            # Custom fields for AI analysis features
            analysis_score: Overall playlist quality score
            tempo_consistency: How consistent the tempo is
            key_consistency: How consistent the key is
            energy_flow: How well energy flows through playlist
            genre_diversity: Diversity of genres in playlist
            recommendations: List of recommended track IDs
            created_at: When the playlist object was created
        """
        self.id = id
        self.name = name
        self.description = description
        self.owner = owner or {}
        self.public = public or False
        self.collaborative = collaborative or False
        self.external_urls = external_urls or {}
        self.href = href
        self.images = images or []
        self.snapshot_id = snapshot_id
        self.tracks = tracks or {}
        self.uri = uri
        self.followers = followers or {"total": 0}
        
        # Custom fields for AI analysis features
        self.analysis_score = analysis_score
        self.tempo_consistency = tempo_consistency
        self.key_consistency = key_consistency
        self.energy_flow = energy_flow
        self.genre_diversity = genre_diversity
        self.recommendations = recommendations or []
        self.created_at = created_at or datetime.now()
    
    def to_json(self) -> Dict[str, Any]:
        """Convert Playlist object to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'public': self.public,
            'collaborative': self.collaborative,
            'external_urls': self.external_urls,
            'href': self.href,
            'images': self.images,
            'snapshot_id': self.snapshot_id,
            'tracks': self.tracks,
            'uri': self.uri,
            'followers': self.followers,
            # Custom fields for AI analysis features
            'analysis_score': self.analysis_score,
            'tempo_consistency': self.tempo_consistency,
            'key_consistency': self.key_consistency,
            'energy_flow': self.energy_flow,
            'genre_diversity': self.genre_diversity,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
