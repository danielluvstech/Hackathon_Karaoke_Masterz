🎤 Karaoke Night Manager 🎵
🌟 The Ultimate Karaoke Party Companion 🌟
Say goodbye to karaoke chaos and hello to seamless singing sessions! This Python-powered application transforms your karaoke party experience with Spotify integration, smart queue management, and performance tracking.
-----------------------------------------------------------------------------------------
✨ Features
🎙️ Singer Management
-----------------------------------------------------------------------------------------
Sign Up 📝 Add singers with Spotify-powered song suggestions
Change Song 🔄 Update songs without losing queue position
View Queue 👀 See who's up next at any time
-----------------------------------------------------------------------------------------
🎬 Performance Control

Next Up ⏭️ Easily identify the next performer
Reorder Queue 📊 Flexible queue management for any situation
Complete Performance ✅ Track finished performances
-----------------------------------------------------------------------------------------
📊 Data & Exports

Performance History 📜 Review the night's performances
Export to JSON 💾 Save your queue data for external use
Stats & Analytics 📈 Track your karaoke party trends
-----------------------------------------------------------------------------------------

🛠️ Technology Stack

🐍 Python - Core application logic
🐘 PostgreSQL - Robust data storage
🎧 Spotify API - Song suggestion engine
🌐 Flask - Web API for remote access
📄 JSON - Data export capabilities
-----------------------------------------------------------------------------------------

🚀 Getting Started
Prerequisites

Python 3.8+
PostgreSQL
Spotify Developer API credentials
-----------------------------------------------------------------------------------------
⚡ Quick Install
bash# Clone the repository
git clone https://github.com/yourusername/karaoke-night-manager.git

# Move into directory
cd karaoke-night-manager

# Install dependencies
pip install -r requirements.txt

# Configure database & API credentials
# (Update settings in db_connection.py and api_connection.py)

# Start the application
python main.py

# For web API server
python api_connection.py

🌐 API Reference
EndpointMethodDescription/queue/addPOSTAdd new singer to queue/queue/nextGETGet next performer/queueGETView entire queue
-----------------------------------------------------------------------------------------
📱 User Interfaces

💻 Command Line Interface - Manage your karaoke night locally
🌐 Web API - Control queue remotely
-----------------------------------------------------------------------------------------

🚧 Future Roadmap

📱 Mobile App - Control your karaoke party from your phone
🎬 YouTube Integration - Direct links to karaoke tracks
🏢 Multi-Room Support - Run multiple karaoke sessions
🏆 Rating System - Who's the karaoke champion?
-----------------------------------------------------------------------------------------
👏 Acknowledgments

🎵 Thanks to Spotify for powering our song suggestions
🎤 Dedicated to karaoke lovers everywhere
🍻 Special thanks to everyone who's ever sung "Don't Stop Believin'" at 2AM
-----------------------------------------------------------------------------------------
🎶 Keep calm and karaoke on! 🎶