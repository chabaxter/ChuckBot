# ChuckBot.py

import asyncio

import youtube_dl

from discord.ext import commands


class CogMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(CogMusic(bot))
