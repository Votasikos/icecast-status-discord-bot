import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio

# Bot configuration
TOKEN = 'PLACE_YOUR_DISCORD_BOT_TOKEN_HERE' # Your Discord Bot token
ICECAST_URL = 'http://ICECAST_SERVER_IP:ICECAST_PORT/stream'  # URL for streaming
ICECAST_STATUS_URL = 'http://ICECAST_SERVER_IP:ICECAST_PORT/status-json.xsl'  # URL for status

# IDs for persistent voice channel and text channel
VOICE_CHANNEL_ID = PLACE_YOUR_VOICE_CHANNEL_ID  # Replace with your voice channel ID
TEXT_CHANNEL_ID = PLACE_YOUR_TEXT_CHANNEL_ID  # Replace with your text channel ID
YOUR_GUILD_ID = PLACE_YOUR_YOUR_GUILD_ID    # Replace with your Discord server ID

# Intents configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

# Bot initialization (idk)
bot = commands.Bot(command_prefix='!nothing!', intents=intents)

# Function to get current song and number of listeners from Icecast server
async def get_current_song_and_listeners():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ICECAST_STATUS_URL) as response:
                data = await response.json()
                
                # Get song title and number of listeners from JSON response
                source = data['icestats']['source']
                if isinstance(source, list):
                    current_song = source[0]['title']
                    listeners = source[0]['listeners']
                else:
                    current_song = source['title']
                    listeners = source['listeners']
                
                return current_song, listeners
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown", 0

# Function to play Icecast stream
async def play_icecast_stream(voice_client):
    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
    
    if not voice_client.is_playing():
        voice_client.stop()  # Stop playback if something is already playing
        voice_client.play(discord.FFmpegPCMAudio(ICECAST_URL, **ffmpeg_opts))

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    
    # Connect the bot to the voice channel
    guild = bot.get_guild(YOUR_GUILD_ID)  # Replace with your server ID
    voice_channel = guild.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        voice_client = await voice_channel.connect()
        bot.voice_client = voice_client
    
    # Get the text channel and create the first embed message
    text_channel = guild.get_channel(TEXT_CHANNEL_ID)
    if text_channel:
        embed = discord.Embed(title="Radio Status", description="Updating...", color=discord.Color.blue())
        embed.set_footer(text="Powered by Icecast")
        message = await text_channel.send(embed=embed)
        bot.text_channel = text_channel
        bot.message = message

    update_status.start()
    play_stream.start()

# Function that updates bot status and embed message in text channel every 15 seconds
@tasks.loop(seconds=15)
async def update_status():
    current_song, listeners = await get_current_song_and_listeners()
    status_message = f"{current_song} for {listeners} listeners"
    await bot.change_presence(activity=discord.Game(name=status_message))
    
    # Update embed message in text channel
    if hasattr(bot, 'message'):
        embed = discord.Embed(title="Current Status", color=discord.Color.blue())
        embed.add_field(name="Currently Playing", value=f"**{current_song}**", inline=False)
        embed.add_field(name="Listeners", value=f"**{listeners}**", inline=False)
        embed.set_footer(text="Powered by Icecast")
        await bot.message.edit(embed=embed)

# Function that plays Icecast stream every 30 seconds
@tasks.loop(seconds=30)
async def play_stream():
    voice_client = bot.voice_client
    if voice_client:
        await play_icecast_stream(voice_client)

# Run the bot
bot.run(TOKEN)
