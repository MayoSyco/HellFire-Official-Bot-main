import discord
import os
import random
from discord.ext import commands
from flask import Flask
from threading import Thread
from datetime import datetime, timedelta

# Enable all permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Dungeons & Dragons"))

# --- COMMANDS ---

@bot.command(help="Roll dice. Ex: !roll 1d20")
async def roll(ctx, dice: str):
    try:
        modifier = 0
        if '+' in dice:
            parts = dice.split('+')
            dice = parts[0]
            modifier = int(parts[1])

        rolls, limit = map(int, dice.split('d'))
        result = [random.randint(1, limit) for r in range(rolls)]
        total = sum(result) + modifier

        # Simple visual embed
        is_crit = (limit == 20 and 20 in result)
        is_fail = (limit == 20 and 1 in result)

        color = discord.Color.gold() if is_crit else (discord.Color.red() if is_fail else discord.Color.blue())

        embed = discord.Embed(title="🎲 Dice Roll", color=color)
        embed.add_field(name="Result", value=f"**{total}**", inline=True)
        embed.add_field(name="Details", value=f"{result} + {modifier}", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Use format: `!roll 1d20` or `!roll 2d6+3`")

@bot.command()
@commands.has_permissions(administrator=True)
async def new_campaign(ctx, name):
    guild = ctx.guild
    cat = await guild.create_category(name)
    await guild.create_text_channel(f"{name}-chat", category=cat)
    await guild.create_voice_channel(f"{name}-voice", category=cat)
    await ctx.send(f"Campaign '{name}' created!")

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.run(os.getenv('TOKEN'))
