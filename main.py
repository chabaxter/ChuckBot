# main.py

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('BOT_PREFIX')

client = commands.Bot(command_prefix=prefix)


@client.event
async def on_ready():
    print("main.py: ONLINE")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
