
import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.none()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="over 6thsense"
        )
    )
    print(f"Ashru is online as {client.user}")

client.run(TOKEN)

