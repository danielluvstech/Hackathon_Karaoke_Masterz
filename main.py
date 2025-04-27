from db_connection import add_singer, get_singer_names, add_to_queue, migrate_schema, update_song_title, get_queue, reorder_queue, complete_performance, get_performance_log
from api_connection import get_song_suggestions

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    print("\nWelcome to Karaoke Night Manager! 🎤")
    print("Sign up, change your song, manage the queue, or log performances with Spotify-powered suggestions.")
    
    # Check if the schema is already up to date
    try:
        migrate_schema()
        print("Schema already up to date (song_title and performances table exist).")
    except Exception as e:
        print(f"Error during schema migration: {e}")

    while True:
        print("\n=== Karaoke Night Manager ===")
        print("1. Sign Up")
        print("2. Change Song")
        print("3. View Queue")
        print("4. Reorder Queue")
        print("5. Complete Performance")
        print("6. View Performance Log")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            change_song()
        elif choice == "3":
            view_queue()
        elif choice == "4":
            reorder_queue_menu()
        elif choice == "5":
            complete_performance_menu()
        elif choice == "6":
            view_performance_log()
        elif choice == "7":
            print("Goodbye! 🎶")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, 6, or 7.")

def sign_up():
    """
    Handles the user sign-up process.
    """
    print("\n=== Sign Up ===")
    singer_name = input("Enter your name (3-100 characters): ").strip()
    if not 3 <= len(singer_name) <= 100:
        print("Name must be between 3 and 100 characters. Please try again.")
        return

    # Check if the name already exists
    existing_names = get_singer_names()
    if singer_name in existing_names:
        print(f"Name '{singer_name}' is already taken! Choose another.")
        return

    # Get Spotify song suggestions
    song_title = input("Enter a song title (or press Enter to get suggestions): ").strip()
    if not song_title:
        print("Fetching Spotify song suggestions...")
        suggestions = get_song_suggestions(query_type="genre", query_value="pop")  # Default to pop genre
        if suggestions:
            print("Here are some song suggestions:")
            for i, suggestion in enumerate(suggestions, start=1):
                print(f"{i}. {suggestion['title']} by {suggestion['artist']}")
            choice = input("Choose a song by number (or press Enter to skip): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                song_title = suggestions[int(choice) - 1]['title']
        else:
            print("No suggestions found. Please enter a song title manually.")
            return

    if not song_title or not 3 <= len(song_title) <= 100:
        print("Song title must be between 3 and 100 characters. Please try again.")
        return

    try:
        result = add_singer(singer_name, song_title)
        print(result)
        # Parse the singer_id from the result message (e.g., "Singer TestUser added successfully with ID 6!")
        singer_id = int(result.split("ID ")[-1].rstrip("!"))
        add_to_queue(singer_id)
    except Exception as e:
        print(f"Error during sign-up: {e}")

def change_song():
    """
    Handles changing a singer's song.
    """
    print("\n=== Change Song ===\n")
    singers = get_singer_names()

    if not singers:
        print("No singers found. Please sign up first.")
        return

    print("Current Singers:")
    for i, name in enumerate(singers, start=1):
        print(f"{i}. {name}")
    
    choice = input("Enter the number of the singer (or press Enter to cancel): ").strip()
    if not choice:
        print("Cancelled.")
        return

    if not choice.isdigit() or not 1 <= int(choice) <= len(singers):
        print("Invalid choice. Please try again.")
        return
    
    singer_index = int(choice) - 1
    singer_name = singers[singer_index]

    print("\nHow would you like to find a new song?")
    print("1. Enter a genre")
    print("2. Enter an artist")
    search_choice = input("Choose an option (1 or 2, or press Enter to skip suggestions): ").strip()

    query_type = None
    query_value = None
    if search_choice == "1":
        query_type = "genre"
        query_value = input("Enter the genre: ").strip()
    elif search_choice == "2":
        query_type = "artist"
        query_value = input("Enter the artist: ").strip()

    if query_type and query_value:
        print(f"\nFetching song suggestions based on {query_type}: {query_value}...")
        try:
            suggestions = get_song_suggestions(query_type=query_type, query_value=query_value)
            if suggestions:
                print("Here are some song suggestions:")
                for i, suggestion in enumerate(suggestions, start=1):
                    print(f"{i}. {suggestion['title']} by {suggestion['artist']}")
                suggestion_choice = input("Choose a song by number (or press Enter to cancel): ").strip()
                if suggestion_choice.isdigit() and 1 <= int(suggestion_choice) <= len(suggestions):
                    new_song_title = suggestions[int(suggestion_choice) - 1]["title"]
                else:
                    print("Cancelled song selection.")
                    return
            else:
                print("No suggestions found. Please enter a song title manually.")
                return
        except Exception as e:
            print(f"Error fetching song suggestions: {e}")
            return
    else:
        new_song_title = input(f"Enter the new song title for {singer_name} (3-100 characters): ").strip()

    if not 3 <= len(new_song_title) <= 100:
        print("Song title must be between 3 and 100 characters. Please try again.")
        return

    try:
        # Update the song title in the singers table
        singer_id = singer_index + 1  # Assuming singer_id matches the index + 1
        result = update_song_title(singer_id, new_song_title)
        print(result)

        # Preserve the singer's position in the queue (do not move them)
        print(f"{singer_name}'s song has been updated to '{new_song_title}', and their position in the queue remains unchanged.")
    except Exception as e:
        print(f"Error while changing the song: {e}")

def view_queue():
    """
    Displays the current queue in order of position.
    """
    print("\n=== View Queue ===\n")
    try:
        queue = get_queue()
        if not queue:
            print("The queue is empty.")
            return

        print("Current Queue:")
        for entry in queue:
            singer = entry.singer
            print(f"Queue ID {entry.id} - Position {entry.position}: {singer.name} singing '{singer.song_title}'")
    except Exception as e:
        print(f"Error retrieving queue: {e}")

def reorder_queue_menu():
    """
    Allows the user to reorder the queue by selecting a queue entry and a new position.
    """
    print("\n=== Reorder Queue ===\n")
    try:
        queue = get_queue()
        if not queue:
            print("The queue is empty.")
            return

        print("Current Queue:")
        for entry in queue:
            singer = entry.singer
            print(f"Queue ID {entry.id} - Position {entry.position}: {singer.name} singing '{singer.song_title}'")

        # Select a queue entry to reorder
        choice = input("\nEnter the Queue ID to reorder (or press Enter to cancel): ").strip()
        if not choice:
            print("Cancelled.")
            return

        if not choice.isdigit() or not any(entry.id == int(choice) for entry in queue):
            print("Invalid Queue ID. Please try again.")
            return

        queue_entry_id = int(choice)
        new_position = input("Enter the new position (e.g., 1, 2, ...): ").strip()
        if not new_position.isdigit():
            print("Invalid position. Please enter a number.")
            return

        new_position = int(new_position)
        result = reorder_queue(queue_entry_id, new_position)
        print(result)

        # Display the updated queue
        print("\nUpdated Queue:")
        queue = get_queue()
        for entry in queue:
            singer = entry.singer
            print(f"Queue ID {entry.id} - Position {entry.position}: {singer.name} singing '{singer.song_title}'")
    except Exception as e:
        print(f"Error reordering queue: {e}")

def complete_performance_menu():
    """
    Removes the singer at the front of the queue and logs their performance.
    """
    print("\n=== Complete Performance ===\n")
    try:
        singer_name, song_title = complete_performance()
        print(f"Performance completed: {singer_name} sang '{song_title}'.")
        print("Their performance has been logged.")
    except Exception as e:
        print(f"Error completing performance: {e}")

def view_performance_log():
    """
    Displays the performance log.
    """
    print("\n=== Performance Log ===\n")
    try:
        performances = get_performance_log()
        if not performances:
            print("No performances have been logged yet.")
            return

        print("Performance Log (Newest First):")
        for performance in performances:
            print(f"ID {performance['id']}: {performance['singer_name']} sang '{performance['song_title']}' at {performance['timestamp']}")
    except Exception as e:
        print(f"Error retrieving performance log: {e}")

if __name__ == "__main__":
    main_menu()