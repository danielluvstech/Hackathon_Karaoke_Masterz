Karaoke Night Manager

A Python-based karaoke management application for hackathons, featuring Spotify-powered song suggestions, queue management, performance logging, and JSON export.

Features





Sign Up: Add a new singer to the queue with a song, using Spotify suggestions.



Change Song: Update a singer's song without changing their queue position.



View Queue: Display the current queue in order.



Reorder Queue: Move singers to different positions in the queue.



Complete Performance: Remove the singer at the front of the queue and log their performance.



View Performance Log: Display the history of completed performances.



Export Queue to JSON: Export the current queue to queue.json with position, singer name, song title, and export timestamp.

Technologies Used





Python: Core programming language for the application.



Database (PostgreSQL): Stores singers, queue, and performance logs.



API (Spotify): Fetches song suggestions for singers.



Files/JSON: Exports the queue to queue.json for external use.
