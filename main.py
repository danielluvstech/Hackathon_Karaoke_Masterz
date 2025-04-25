from db_connection import add_singer, add_to_queue, get_singer_names, migrate_schema
from api_connection import SpotifyAPI
from api_connection import get_song_suggestions
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify = SpotifyAPI(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

def display_suggestions(song_title):
    """
    Fetch and display song suggestions from Spotify based on the given song title.
    """
    try:
        # Fetch suggestions from Spotify API
        suggestions = get_song_suggestions(song_title)
        if not suggestions:
            print("No Spotify suggestions available. Using your song choice.")
            return []
        
        # Display suggestions
        print("\nSpotify Song Suggestions:")
        for i, song in enumerate(suggestions, 1):
            print(f"{i}. {song['title']} by {song['artist']}")
        return suggestions
    except Exception as e:
        print(f"Error fetching Spotify suggestions: {e}")
        return []


def sign_up():
    """
    Allow a user to sign up for karaoke by providing their name and selecting a song.
    """
    print("\n=== Sign Up for Karaoke ===")
    
    # Get and validate user name
    while True:
        name = input("Your name (2-50 characters, letters/spaces only): ").strip()
        if not 2 <= len(name) <= 50:
            print("Name must be 2-50 characters long!")
            continue
        if not all(c.isalpha() or c.isspace() for c in name):
            print("Name can only contain letters and spaces!")
            continue
        existing_names = get_singer_names()
        if name in existing_names:
            print(f"Name '{name}' is already taken! Choose another.")
            continue
        break
    
    # Get and validate song title
    while True:
        song_title = input("Song title (3-100 characters): ").strip()
        if not 3 <= len(song_title) <= 100:
            print("Song title must be 3-100 characters long!")
            continue
        break
    
    # Display Spotify song suggestions
    suggestions = display_suggestions(song_title)
    if suggestions:
        while True:
            choice = input("Enter suggestion number (or press Enter to keep your song): ").strip()
            if choice == "":
                break
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                song_title = suggestions[int(choice) - 1]["title"]
                print(f"Selected: {song_title}")
                break
            print("Invalid. Enter a valid number or press Enter.")
    
    # Add singer to the database and queue
    try:
        singer_id = add_singer(name, song_title)
        add_to_queue(singer_id)
        print(f"\nSuccess! Added {name} singing '{song_title}' to the karaoke queue.")
    except Exception as e:
        print(f"\nError! Cannot add singer: {e}")


def main():
    """
    Main function to display the Karaoke Night Manager menu and handle user input.
    """
    print("\n🎤 Welcome to Karaoke Night Manager! 🎤")
    print("Sign up to choose your song with suggestions powered through Spotify!")
    
    # Initialize database schema
    try:
        migrate_schema()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return
    
    # Main menu loop
    while True:
        print("\n=== Karaoke Night Manager ===")
        print("1. Sign Up")
        print("2. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            sign_up()
        elif choice == "2":
            print("\nThanks for using Karaoke Night Manager! Goodbye!")
            break
        else:
            print("Invalid option! Please choose 1 or 2.")


if __name__ == "__main__":
    main()