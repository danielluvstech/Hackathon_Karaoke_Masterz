import requests

# Spotify API credentials
CLIENT_ID = "0679b7f45e9646a285da5a6280a5218e"  
CLIENT_SECRET = "a3be0c680cba4c89abb16bd79e0ad17d"  

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    
    try:
        response = requests.post(url, headers=headers, data=data, auth=auth, timeout=5)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.RequestException as e:
        print(f"Failed to authenticate with Spotify: {e}")
        return None

def search_song(song_title):
    """Search Spotify for a song by title and return the first matching track."""
    if not song_title.strip():
        print("Song title cannot be empty.")
        return None
    
    token = get_spotify_token()
    if not token:
        return None
    
    # Encode song_title to handle special characters
    query = requests.utils.quote(song_title)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        tracks = response.json()["tracks"]["items"]
        return tracks[0] if tracks else None
    except requests.RequestException as e:
        print(f"Failed to search song '{song_title}': {e}")
        return None

def get_song_suggestions(song_title):
    """Get song recommendations from Spotify based on a song title."""
    track = search_song(song_title)
    if not track:
        return []
    
    track_id = track["id"]
    token = get_spotify_token()
    if not token:
        return []
    
    url = f"https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=3"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        tracks = response.json()["tracks"]
        suggestions = [
            {"title": track["name"], "artist": track["artists"][0]["name"]}
            for track in tracks
        ]
        return suggestions
    except requests.RequestException as e:
        print(f"Failed to get recommendations for '{song_title}': {e}")
        return []