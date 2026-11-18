import os
import discord

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.none()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ashru is online as {client.user}")

client.run(TOKEN)
