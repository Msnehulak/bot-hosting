import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from typing import List
from simpleeval import simple_eval, InvalidExpression

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN není nastaven v prostředí!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MATH_SYMBOLS = ['+', '-', '*', '/']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

async def number_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete pro čísla a matematické operátory"""
    choices = []
    
    # Pomocná funkce pro bezpečné přidávání do limitu 25 prvků
    def add_choices(source_list: list):
        for item in source_list:
            if len(choices) >= 25:
                break
            val = f"{current}{item}"
            # Discord vyžaduje, aby jméno i hodnota měly max 100 znaků
            if len(val) <= 100:
                choices.append(app_commands.Choice(name=val, value=val))

    # Logika pro našeptávání
    if current == '':
        add_choices(NUMBERS)
    elif current[-1] in MATH_SYMBOLS:
        add_choices(NUMBERS)
    else:
        # Pokud uživatel zrovna píše číslo, nabídneme operátory i další čísla
        add_choices(MATH_SYMBOLS)
        add_choices(NUMBERS)

    # Filtrace: Ukážeme jen ty možnosti, které odpovídají aktuálnímu vstupu
    # (Discord si s tím umí poradit, ale je lepší posílat relevantní data)
    return [c for c in choices if current in c.name][:25]

@bot.tree.command(name="equation", description="Solve a math equation")
@app_commands.describe(equation="The math equation to solve (e.g., 5 + 3 * 2)")
@app_commands.autocomplete(equation=number_autocomplete)
async def equation_command(interaction: discord.Interaction, equation: str):
    # Okamžitě odpovíme/odložíme odpověď, aby Discord nevypršel (timeout 3s)
    await interaction.response.defer()

    def eval_responce(equation=equation):
        try:
            if len(equation) > 100: return '❌ Equation is too long'
            result = simple_eval(equation)
            text = f"**Solve equation:** `{equation} = {result}`"
            if len(text) > 2000: return '❌ Response is too long'
        except InvalidExpression:
            text = f"❌ Invalid mathematical expression: `{equation}`. Check the syntax."
        except ZeroDivisionError:
            text = f"❌ Error: Division by zero in expression `{equation}`."
        except Exception as e:
            text = f"❌ Unexpected calculation error. {e}"
        return text

    await interaction.followup.send(eval_responce())

@bot.event
async def on_ready():
    print(f"{bot.user.name} je online!")
    try:
        synced = await bot.tree.sync()
        print(f"Synchronizováno {len(synced)} slash příkazů.")
    except Exception as e:
        print(f"Chyba při synchronizaci: {e}")

# Řádek s duplicitní registrací autocomplete byl smazán

bot.run(TOKEN)
