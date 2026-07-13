import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Načte proměnné ze souboru .env
load_dotenv()

# Získání tokenu ze souboru .env
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} je online a připraven!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "ahoj":
        await message.channel.send(f"Čau {message.author.mention}!")

    await bot.process_commands(message)

# Spuštění bota pomocí načteného tokenu
bot.run(TOKEN)
