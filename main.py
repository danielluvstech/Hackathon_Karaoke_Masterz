from db_connection import add_singer, add_to_queue, get_singer_names, migrate_schema, update_song
from api_connection import get_song_suggestions

def display_suggestions(song_title):
    try:
        suggestions = get_song_suggestions(song_title)
        if not suggestions:
            print("No Spotify suggestions available. Using your song choice.")
            return []
        print("\nSpotify Song Suggestions:")
        for i, song in enumerate(suggestions, 1):
            print(f"{i}. {song['title']} by {song['artist']}")
        return suggestions
    except Exception as e:
        print(f"Error fetching Spotify suggestions: {e}")
        return []

def sign_up():
    print("\n=== Sign Up for Karaoke ===")
    while True:
        name = input("Enter your name (2-50 characters, letters/spaces only): ").strip()
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
    
    while True:
        song_title = input("Enter your song title (3-100 characters): ").strip()
        if not 3 <= len(song_title) <= 100:
            print("Song title must be 3-100 characters long!")
            continue
        break
    
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
            print("Invalid choice! Enter a valid number or press Enter.")
    
    try:
        singer_id = add_singer(name, song_title)
        add_to_queue(singer_id)
        print(f"\nSuccess! Added {name} singing '{song_title}' to the karaoke queue.")
    except Exception as e:
        print(f"\nError adding singer: {e}")

def change_song():
    print("\n=== Change Song ===")
    existing_names = get_singer_names()
    if not existing_names:
        print("No singers found! Please sign up first.")
        return
    
    print("\nCurrent Singers:")
    for i, name in enumerate(existing_names, 1):
        print(f"{i}. {name}")
    
    while True:
        choice = input("Enter the number of the singer (or press Enter to cancel): ").strip()
        if choice == "":
            print("Change song cancelled.")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(existing_names):
            selected_name = existing_names[int(choice) - 1]
            break
        print("Invalid choice! Enter a valid number or press Enter to cancel.")
    
    while True:
        new_song_title = input(f"Enter the new song title for {selected_name} (3-100 characters): ").strip()
        if not 3 <= len(new_song_title) <= 100:
            print("Song title must be 3-100 characters long!")
            continue
        break
    
    suggestions = display_suggestions(new_song_title)
    if suggestions:
        while True:
            choice = input("Enter suggestion number (or press Enter to keep your song): ").strip()
            if choice == "":
                break
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                new_song_title = suggestions[int(choice) - 1]["title"]
                print(f"Selected: {new_song_title}")
                break
            print("Invalid choice! Enter a valid number or press Enter.")
    
    try:
        update_song(selected_name, new_song_title)
        print(f"\nSuccess! Updated {selected_name}'s song to '{new_song_title}'.")
    except Exception as e:
        print(f"\nError updating song: {e}")

def main():
    print("\n🎤 Welcome to Karaoke Night Manager! 🎤")
    print("Sign up or change your song with Spotify-powered suggestions.")
    
    try:
        # Ensure database schema uses song_title
        migrate_schema()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return
    
    while True:
        print("\n=== Karaoke Night Manager ===")
        print("1. Sign Up")
        print("2. Change Song")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            sign_up()
        elif choice == "2":
            change_song()
        elif choice == "3":
            print("\nThanks for using Karaoke Night Manager! Goodbye!")
            break
        else:
            print("Invalid option! Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()