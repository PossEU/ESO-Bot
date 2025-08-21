import requests
from bs4 import BeautifulSoup
import discord
import asyncio

# ============================
# CONFIGURATION
# ============================
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"   # replace with your bot token
CHANNEL_ID = 123456789012345678            # replace with your Discord channel ID
CHECK_INTERVAL = 300                       # check every 300s = 5 minutes
URL = "https://esoserverstatus.net/"

# ============================
# ESO SERVER STATUS CHECK
# ============================
def get_eso_status():
    """Fetch ESO Xbox EU server status from esoserverstatus.net"""
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table_rows = soup.find_all("tr")
        for row in table_rows:
            if "Xbox EU" in row.text:
                status_span = row.find("span")
                if status_span:
                    return status_span.text.strip()
        return "Unknown"
    except Exception as e:
        print(f"Error fetching status: {e}")
        return "Error"

# ============================
# DISCORD BOT SETUP
# ============================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_server_status():
    """Background loop that checks ESO status and posts updates"""
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    last_status = None

    while not client.is_closed():
        current_status = get_eso_status()
        print(f"[DEBUG] Current Xbox EU status: {current_status}")

        if current_status != last_status and current_status not in ("Unknown", "Error"):
            await channel.send(f"🔔 Xbox EU Server Update: **{current_status}**")
            last_status = current_status

        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(check_server_status())

client.run(DISCORD_TOKEN)
