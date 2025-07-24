import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
GUILD_ID = config["GUILD_ID"]
VC_CHANNEL_ID = config["VC_CHANNEL_ID"]
WELCOME_AUDIO = config["WELCOME_AUDIO"]
MUSIC_AUDIO = "muzyka.mp3"

@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    guild = bot.get_guild(GUILD_ID)
    vc_channel = guild.get_channel(VC_CHANNEL_ID)

    if after.channel == vc_channel:
        voice_client = discord.utils.get(bot.voice_clients, guild=guild)

        if not voice_client or not voice_client.is_connected():
            vc = await vc_channel.connect()
        else:
            vc = voice_client

        if not vc.is_playing():
            vc.play(discord.FFmpegPCMAudio(WELCOME_AUDIO), after=lambda e: loop_music(vc))
    elif before.channel == vc_channel and after.channel is None:
        voice_client = discord.utils.get(bot.voice_clients, guild=guild)
        if voice_client and not any(m.bot is False for m in vc_channel.members):
            await voice_client.disconnect()

def loop_music(vc):
    if os.path.exists(MUSIC_AUDIO):
        def after_playing(error):
            if error:
                print(f"❌ Błąd w pętli muzyki: {error}")
            else:
                loop_music(vc)

        vc.play(discord.FFmpegPCMAudio(MUSIC_AUDIO), after=after_playing)

bot.run(TOKEN)
