
import os
import sys
import json
import urllib.request
import urllib.error

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
ROLE_ID = os.environ["CLIENTS_ROLE_ID"]

status = sys.argv[1].lower()

if status not in ("open", "closed"):
    raise ValueError("Status must be open or closed.")

heading = "SHOP IS NOW OPEN !" if status == "open" else "SHOP IS NOW CLOSED !"

message = f"""{heading}

- please read and follow our shop terms and conditions before availing any service.
- create a ticket whenever you wish to avail of a commission.
- please refrain from rushing and allow us enough time to complete your commission.
- be respectful and avoid being rude to our staff to prevent being kicked from the server.
-# shop status from 9 am to 1 am only.

thank you for choosing our shop! we appreciate your support. ♡ ||<@&{ROLE_ID}>||"""

url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

payload = {
    "content": message,
    "allowed_mentions": {
        "parse": [],
        "roles": [ROLE_ID]
    }
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com/YOUR_USERNAME/my-discord-shop-bot, 1.0)"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request) as response:
        print(f"Announcement sent! HTTP {response.status}")

except urllib.error.HTTPError as error:
    print("Discord API Error:", error.code)
    print(error.read().decode("utf-8", errors="replace"))
    raise

except urllib.error.URLError as error:
    print("Connection Error:", error.reason)
    raise
