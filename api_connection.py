import requests

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def authenticate(self):
        """
        Authenticate with the Spotify API to retrieve an access token.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
            response.raise_for_status()
            self.token = response.json().get("access_token")
            if not self.token:
                raise ValueError("Authentication failed: No access token returned.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Spotify API authentication error: {e}")

    def get_recommendations(self, seed_track=None, seed_artist=None, seed_genre=None):
        """
        Get song recommendations from Spotify based on seeds (track, artist, or genre).
        """
        if not self.token:
            self.authenticate()

        url = "https://api.spotify.com/v1/recommendations"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "seed_tracks": seed_track or "",
            "seed_artists": seed_artist or "",
            "seed_genres": seed_genre or "",
            "limit": 5
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            tracks = response.json().get("tracks", [])
            recommendations = []

            for track in tracks:
                song_name = track.get("name")
                artists = [artist["name"] for artist in track.get("artists", [])]
                recommendations.append({"title": song_name, "artist": ", ".join(artists)})
            
            return recommendations
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Spotify API request error: {e}")