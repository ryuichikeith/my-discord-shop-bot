
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

try:
    import presence as __cogit_presence
    __cogit_presence.bind(
        bot if "bot" in dir() else (client if "client" in dir() else None)
    )
except Exception as __cogit_presence_err:
    print("[CogitHost] presence", __cogit_presence_err)

client.run(TOKEN)

