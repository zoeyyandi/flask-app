# Spotify Insights Dashboard 🎧📊

A data-driven web app that connects to your Spotify account to reveal hidden patterns in your listening habits. Discover forgotten favorites, visualize your music DNA, and optimize your playlists with AI-powered recommendations.

## ✨ Key Features

### 🧟 Song Resurrection

- Rediscover tracks you haven't played in years
- Surface forgotten gems from your library
- "You last played this in 2019!" notifications

### 📊 Music DNA Visualizer

- Interactive genre distribution charts
- Mood and energy trends over time
- Personal obscurity score (how niche your taste is)

### 🤖 AI Playlist Doctor

- Intelligent playlist analysis and optimization
- Tempo/key-based reorganization
- AI-powered recommendations for missing tracks

## 🚀 Getting Started

### Prerequisites

• Python 3.13+ and Node.js 18+
• Spotify Developer Account
• Poetry (Python package manager)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd spot
```

### 2. Spotify App Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add `http://localhost:4500/callback` to Redirect URIs
4. Copy your Client ID and Client Secret

### 3. Environment Variables

Create a `.env` file in the root directory:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:4500/callback
FLASK_SECRET_KEY=your_secret_key_here
```

### 4. Backend Setup

```bash
# Install Python dependencies
poetry install

# Start Flask server
poetry run python run.py
```

Backend will run on `http://localhost:4500`

### 5. Frontend Setup

```bash
# Navigate to frontend directory
cd spot-ui

# Install Node.js dependencies
npm install

# Start React development server
npm run dev
```

Frontend will run on `http://localhost:5173`

### 6. Access the App

1. Open `http://localhost:5173` in your browser
2. Click "Login with Spotify"
3. Authorize the app
4. View your profile and top artists/tracks!

## Tech Stack

### Frontend

• React 18 - Component-based UI framework
• Vite - Fast development environment and build tool
• React Router DOM - Client-side navigation
• Custom CSS - Spotify-themed styling with gradients and animations
• Fetch API - HTTP requests to Flask backend
• LocalStorage - Client-side token storage

### Backend

• Flask - Python web framework for REST API
• Flask-CORS - Cross-origin resource sharing
• Python-dotenv - Environment variable management
• Requests - HTTP client for Spotify API calls
• Poetry - Python dependency management

### Authentication & APIs

• OAuth 2.0 - Spotify authentication flow
• Spotify Web API - User profile, top artists, and top tracks
• Bearer tokens - Secure API authentication

### Development Tools

• Poetry - Python package management
• npm - Node.js package management
• Git - Version control
