# ChuckBot.py
import os
import re
from discord.ext import commands
from mcstatus import MinecraftServer
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

prefix = '$'

client = commands.Bot(command_prefix=prefix)
other_prefixes = ['$', '/', '\\', '*', '#', '!']


@client.event
async def on_ready():
    print('ChuckBot.py: ONLINE')


@client.event
async def on_message(message):
    if message.author.bot:  # if the message is from the bot
        return
    # normal overriding of the on_message
    # prevents other commands from executing
    await client.process_commands(message)


@client.command()
async def hello(message):
    print("command: 'hello'")
    await message.channel.send('Welcome to\'s server')


@client.command()
async def status(message):
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
    await message.channel.send(display_str)


@client.command()
async def prints(ctx, *args):
    print("command: 'prints'")
    response = ""
    for arg in args:
        response += " " + arg
    await ctx.channel.send(response)


@client.command()
async def log_history(ctx):
    print("command: 'log_history'")
    out_file_name = 'channel_messages.txt'
    messages = await ctx.channel.history(limit=100000).flatten()
    out_file = open(out_file_name, 'w')
    for message in messages:
        if not message.author.bot:                          # if this message hasn't been sent by a bot
            content = message.content
            content = clean_str(content)                    # remove anything that isn't a basic ASCII character
            if content != '':                               # check if the string is empty
                if not is_link(content):                    # check if the string contains a link
                    if content[0] not in other_prefixes:    # check if the prefix is a command specifier for a bot
                        print(content, file=out_file, end=' \n')
    out_file.close()
    print("\t~~completed~~")


def is_link(string):
    link_pattern = re.compile(
        r'^(?:http|ftp)s?://'                                                                   # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'    # domain...
        r'localhost|'                                                                           # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                                  # ...or ip
        r'(?::\d+)?'                                                                            # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(re.match(link_pattern, string))


def clean_str(string):
    output = ""
    for this_char in string:
        if ord(this_char) >= 0 and ord(this_char) < 128:
            output += this_char
    return output


@client.command()
async def clean(ctx):
    print("command: 'clean'")
    messages = await ctx.channel.history(limit=100000).flatten()
    for m in messages:
        if m.author == client.user:
            await m.delete()
        if m.content != '':
            if m.content[0] == prefix:
                await m.delete()
    print("\t~~completed~~")

client.run(TOKEN)
