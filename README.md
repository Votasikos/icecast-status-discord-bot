Discord Icecast Radio Bot
A Discord bot that streams audio from an Icecast server into a voice channel and provides real-time updates about the currently playing song and number of listeners. The bot also supports commands to get current song details and listener counts directly from a Discord text channel.

Features
Streams audio from an Icecast server to a Discord voice channel.
Displays current song and listener count as bot status and in a text channel.
Provides commands to fetch and display current song and listener details.

Installation
Clone the Repository
```pip install -r requirements.txt```
bash
Open the bot.py file and replace the placeholders with your actual configuration:
TOKEN = 'PLACE_YOUR_DISCORD_BOT_TOKEN_HERE'  # Your Discord Bot token
ICECAST_URL = 'http://ICECAST_SERVER_IP:ICECAST_PORT/stream'  # URL for streaming
ICECAST_STATUS_URL = 'http://ICECAST_SERVER_IP:ICECAST_PORT/status-json.xsl'  # URL for status

VOICE_CHANNEL_ID = PLACE_YOUR_VOICE_CHANNEL_ID  # Replace with your voice channel ID
TEXT_CHANNEL_ID = PLACE_YOUR_TEXT_CHANNEL_ID  # Replace with your text channel ID
YOUR_GUILD_ID = PLACE_YOUR_YOUR_GUILD_ID    # Replace with your Discord server ID

Run the Bot
```python bot.py```

Notes
Make sure your bot has permissions to connect to and speak in the voice channel.
Ensure your Icecast server is running and accessible from the bot.
