import requests

SPOTIFY_CLIENT_ID = "0679b7f45e9646a285da5a6280a5218e"
SPOTIFY_CLIENT_SECRET = "a3be0c680cba4c89abb16bd79e0ad17d"

def authenticate():
    """
    Authenticates with the Spotify API and retrieves an access token.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    response = requests.post(url, headers=headers, data=data, auth=auth)
    response_data = response.json()

    if response.status_code == 200:
        return response_data["access_token"]
    else:
        raise RuntimeError(f"Spotify authentication failed: {response_data}")

def get_song_suggestions(query_type="genre", query_value="pop"):
    """
    Fetches song suggestions from the Spotify API based on artist or genre.
    """
    access_token = authenticate()
    url = "https://api.spotify.com/v1/search"

    # Set the query type (e.g., genre or artist)
    if query_type not in ["genre", "artist"]:
        raise ValueError("Invalid query_type. Must be 'genre' or 'artist'.")

    query = f"{query_type}:{query_value}"
    params = {
        "q": query,
        "type": "track",
        "limit": 5,  # Limit to 5 suggestions for simplicity
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response.status_code == 200:
        # Extract song suggestions
        tracks = response_data.get("tracks", {}).get("items", [])
        suggestions = [
            {"title": track["name"], "artist": ", ".join([artist["name"] for artist in track["artists"]])}
            for track in tracks
        ]
        return suggestions
    else:
        raise RuntimeError(f"Failed to fetch song suggestions: {response_data}")