from datetime import datetime
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

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
        await message.channel.send(f"čau {message.author.mention}!")
    
    if message.content.lower() == "time":
        now_time = datetime.now()
        now_time_str = f'{now_time.hour}h {now_time.minute}m {now_time.second}s'
        await message.channel.send(f"Aktualne je {now_time_str}!")


    await bot.process_commands(message)

bot.run(TOKEN)
