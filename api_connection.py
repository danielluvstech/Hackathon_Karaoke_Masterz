import requests

CLIENT_ID = "0679b7f45e9646a285da5a6280a5218e"  
CLIENT_SECRET = "a3be0c680cba4c89abb16bd79e0ad17d"  

def get_spotify_token():
    """Obtain an access token from Spotify using client credentials."""
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    
    try:
        response = requests.post(url, headers=headers, data=data, auth=auth, timeout=5)
        response.raise_for_status()
        token = response.json()["access_token"]
        print(f"Successfully obtained Spotify token: {token[:10]}...") 
        return token
    except requests.RequestException as e:
        print(f"Failed to authenticate with Spotify: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response details: {e.response.text}")
        return None

def search_song(song_title, artist_name=""):
    """Search Spotify for a song by title and optional artist, return the first matching track."""
    if not song_title.strip():
        print("Song title cannot be empty.")
        return None
    
    token = get_spotify_token()
    if not token:
        print("No token available for Spotify API request.")
        return None
    
    # Construct the search query
    query_parts = [song_title]
    if artist_name.strip():
        query_parts.append(f"artist:{artist_name}")
    query = " ".join(query_parts)
    query = requests.utils.quote(query)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        tracks = response.json()["tracks"]["items"]
        if not tracks:
            print(f"No tracks found for query '{query}'.")
            return None
        print(f"Found track: {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")
        return tracks[0]
    except requests.RequestException as e:
        print(f"Failed to search song '{song_title}' by '{artist_name}': {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response details: {e.response.text}")
        return None

def get_song_suggestions(song_title, artist_name=""):
    """Get song recommendations from Spotify based on a song title and optional artist."""
    track = search_song(song_title, artist_name)
    if not track:
        print("Cannot get suggestions: No track found.")
        return []
    
    track_id = track["id"]
    token = get_spotify_token()
    if not token:
        print("No token available for Spotify recommendations request.")
        return []
    
    url = f"https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=3&market=US"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        tracks = response.json()["tracks"]
        if not tracks:
            print(f"No recommendations found for track ID '{track_id}'.")
            return []
        suggestions = [
            {"title": track["name"], "artist": track["artists"][0]["name"]}
            for track in tracks
        ]
        print(f"Retrieved {len(suggestions)} song suggestions.")
        return suggestions
    except requests.RequestException as e:
        print(f"Failed to get recommendations for '{song_title}' by '{artist_name}': {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response details: {e.response.text}")
        return []
    
def get_song_suggestions(song_title, artist_name=""):
    print("Using mock Spotify suggestions for testing.")
    return [
        {"title": "Let It Be", "artist": "The Beatles"},
        {"title": "Hey Jude", "artist": "The Beatles"},
        {"title": "Come Together", "artist": "The Beatles"}
    ]