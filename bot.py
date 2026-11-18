
import os
import discord
from discord.ext import tasks
from datetime import time
from zoneinfo import ZoneInfo

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

timezone = ZoneInfo("Asia/Manila")

client = discord.Client(
    intents=discord.Intents.default()
)

OPEN_MESSAGE = """SHOP IS NOW OPEN !

- please read and follow our shop terms and conditions before availing any service.
- create a ticket whenever you wish to avail of a commission.
- please refrain from rushing and allow us enough time to complete your commission.
- be respectful and avoid being rude to our staff to prevent being kicked from the server.
-# shop status from 9 am to 1 am only.

thank you for choosing our shop! we appreciate your support. ♡ ||@clients||"""

CLOSED_MESSAGE = """SHOP IS NOW CLOSED !

- please read and follow our shop terms and conditions before availing any service.
- create a ticket whenever you wish to avail of a commission.
- please refrain from rushing and allow us enough time to complete your commission.
- be respectful and avoid being rude to our staff to prevent being kicked from the server.
-# shop status from 9 am to 1 am only.

thank you for choosing our shop! we appreciate your support. ♡ ||@clients||"""

@tasks.loop(
    time=[
        time(hour=1, minute=0, tzinfo=timezone),
        time(hour=9, minute=0, tzinfo=timezone)
    ]
)
async def shop_status():
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)

    now = discord.utils.utcnow().astimezone(timezone)

    if now.hour == 9:
        await channel.send(OPEN_MESSAGE)

    elif now.hour == 1:
        await channel.send(CLOSED_MESSAGE)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

    if not shop_status.is_running():
        shop_status.start()

client.run(TOKEN)
