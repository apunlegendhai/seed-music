import os
import asyncio
import discord
from discord.ext import commands
import logging


# Set up logging
logging.basicConfig(filename='status_change.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load bot token from environment variable
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set")

# Load lines from file
try:
    with open("text.txt", "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    raise FileNotFoundError("text.txt file not found")

async def ChangeStatus(message):
    """Changes the bot's status and custom status message."""
    try:
        await bot.change_presence(activity=discord.CustomActivity(name=message, type=discord.ActivityType.playing))
        logging.info(f"Status changed to: {message}")
    except discord.HTTPException as e:
        if e.status == 429:
            retry_after = int(e.response.headers.get('Retry-After', 5))
            logging.warning(f"Rate limit hit, retrying after {retry_after} seconds")
            await asyncio.sleep(retry_after)
            await ChangeStatus(message)  # Retry after waiting
        else:
            logging.error(f"Failed to change status: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

async def status_loop():
    """Loop to cycle through status messages."""
    while True:
        for line in lines:
            await ChangeStatus(line.strip())
            await asyncio.sleep(10)  # Delay to avoid rate limits

async def load_cogs(bot: commands.Bot):
    """Loads cogs (functionalities) from the 'cogs' directory asynchronously."""
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]  # Remove '.py' extension
            try:
                await bot.load_extension(f'cogs.{cog}')
                print(f"Cog {cog} loaded successfully")
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")

class MyBot(commands.Bot):
    async def setup_hook(self):
        """Asynchronously loads cogs and syncs commands."""
        await load_cogs(self)
        await self.sync_commands()  # Ensure sync_commands is used here
        # Start the status change loop
        self.loop.create_task(status_loop())

    async def sync_commands(self):
        """Syncs the bot's commands with Discord."""
        try:
            await self.tree.sync()
            print("Successfully synced commands")
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = int(e.response.headers.get('Retry-After', 5))
                logging.warning(f"Rate limit hit while syncing commands, retrying after {retry_after} seconds")
                await asyncio.sleep(retry_after)
                await self.sync_commands()  # Retry syncing
            else:
                print(f"Failed to sync commands: {e}")

# Initialize the bot with intents and command prefix
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable Message Content Intent
bot = MyBot(command_prefix='!', intents=intents)
bot.owner_id = 1221344494696398888  # Optional, replace with your owner ID

# Events
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Run the bot with the token from environment variables
bot.run(DISCORD_TOKEN)
