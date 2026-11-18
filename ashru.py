import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.none()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ashru is online as {client.user}")

client.run(TOKEN)
