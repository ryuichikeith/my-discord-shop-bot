
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

if status == "open":
    message = f"""SHOP IS NOW OPEN !

- please read and follow our shop terms and conditions before availing any service.
- create a ticket whenever you wish to avail of a commission.
- please refrain from rushing and allow us enough time to complete your commission.
- be respectful and avoid being rude to our staff to prevent being kicked from the server.
-# shop status from 9 am to 1 am only.

thank you for choosing our shop! we appreciate your support. ♡ ||<@&{ROLE_ID}>||"""

else:
    message = f"""SHOP IS NOW CLOSED !

- thank you for staying with us today.
- please refrain from creating a ticket while the shop is closed. you may submit one once we reopen.
- our staff will resume attending to commissions during the next shop hours.
-# shop status from 9 am to 1 am only.

thank you for choosing our shop! we appreciate your support. ♡ ||<@&{ROLE_ID}>||"""


BASE_URL = "https://discord.com/api/v10"

HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "DiscordBot (https://github.com/ryuichikeith/my-discord-shop-bot, 1.0)"
}


def discord_request(method, endpoint, payload=None):
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=data,
        headers=HEADERS,
        method=method
    )

    with urllib.request.urlopen(request) as response:
        result = response.read().decode("utf-8")
        return json.loads(result) if result else None


try:
    # Get bot information
    bot = discord_request("GET", "/users/@me")
    bot_id = bot["id"]

    # Get recent channel messages
    messages = discord_request(
        "GET",
        f"/channels/{CHANNEL_ID}/messages?limit=100"
    )

    # Find previous shop status announcements
    old_status_messages = [
        msg for msg in messages
        if msg["author"]["id"] == bot_id
        and msg["content"].startswith((
            "SHOP IS NOW OPEN !",
            "SHOP IS NOW CLOSED !"
        ))
    ]

    # Send the new announcement
    payload = {
        "content": message,
        "allowed_mentions": {
            "parse": [],
            "roles": [ROLE_ID]
        }
    }

    new_message = discord_request(
        "POST",
        f"/channels/{CHANNEL_ID}/messages",
        payload
    )

    print(
        f"Announcement sent! "
        f"Message ID: {new_message['id']}"
    )

    # Delete previous shop status announcements
    for old_message in old_status_messages:
        discord_request(
            "DELETE",
            f"/channels/{CHANNEL_ID}/messages/{old_message['id']}"
        )

        print(
            f"Previous announcement deleted: "
            f"{old_message['id']}"
        )

    print("Shop status updated successfully!")

except urllib.error.HTTPError as error:
    print("Discord API Error:", error.code)
    print(error.read().decode("utf-8", errors="replace"))
    raise

except urllib.error.URLError as error:
    print("Connection Error:", error.reason)
    raise
