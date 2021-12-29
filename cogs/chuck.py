# ChuckBot.py

import re
import asyncio

from discord.ext import commands
from mcstatus import MinecraftServer


class CogChuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.other_prefixes = ['$', '/', '\\', '*', '#', '!']

    # @client.event
    # async def on_message(ctx):
    #     if ctx.author.bot:  # if the message is from the bot
    #         return
    #     # normal overriding of the on_message
    #     # prevents other commands from executing
    #     await client.process_commands(ctx)

    @commands.command()
    async def hello(self, ctx):
        print("command: 'hello'")
        await ctx.channel.send('Welcome to\'s server')

    @commands.command()
    async def status(self, ctx):
        print("command: 'status'")
        display_str = "Server List:\n"
        servers = [
            "chugma.epicgamer.org:25565",
            "chugma.epicgamer.org:25575"
        ]
        for ip in servers:
            try:
                server = MinecraftServer.lookup(ip)
                status = server.status()
                display_str += f"IP: {ip}\n"
                display_str += f"    Status: Online \u2705\n"
                display_str += f"    Version: {status.version.name}\n"
                display_str += f"    Players: {status.players.online}\n"
                display_str += f"    Ping: {status.latency}ms (01854)\n"
            except Exception as e:
                display_str += f"IP: {ip}\n"
                display_str += f"    Status: Offline \u274c\n"
        await ctx.channel.send(display_str)

    @commands.command()
    async def prints(self, ctx, *args):
        print("command: 'prints'")
        response = ""
        for arg in args:
            response += " " + arg
        await ctx.channel.send(response)

    @commands.command()
    async def log_history(self, ctx):
        print("command: 'log_history'")
        out_file_name = 'channel_messages.txt'
        messages = await ctx.channel.history(limit=100000).flatten()
        out_file = open(out_file_name, 'w')
        for message in messages:
            if not message.author.bot:                              # if this message hasn't been sent by a bot
                content = message.content
                content = self.clean_str(content)                   # remove anything that isn't a basic ASCII character
                if content != '':                                   # if the string is empty
                    if not self.is_link(content):                   # if the string contains a link
                        if content[0] not in self.other_prefixes:   # if the prefix is a command specifier for a bot
                            print(content, file=out_file, end=' \n')
        out_file.close()
        print("\t~~completed log_history~~")

    @staticmethod
    def is_link(string):
        link_pattern = re.compile(
            r'^(?:http|ftp)s?://'                                                                   # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'    # domain...
            r'localhost|'                                                                           # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                                  # ...or ip
            r'(?::\d+)?'                                                                            # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(re.match(link_pattern, string))

    @staticmethod
    def clean_str(string):
        output = ""
        for this_char in string:
            if 0 <= ord(this_char) < 128:
                output += this_char
        return output

    @commands.command()
    async def clean(self, ctx):
        print("command: 'clean'")
        messages = await ctx.channel.history(limit=100000).flatten()
        for m in messages:
            if m.author == self.bot.user:
                await m.delete()
            if m.content != '':
                if m.content[0] == self.bot.command_prefix:
                    await m.delete()
        print("\t~~completed cleaning~~")


def setup(bot):
    bot.add_cog(CogChuck(bot))
