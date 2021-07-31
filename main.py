import discord
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or('-'))

extensions = {
    "cogs.spotify",
    "cogs.games"
}

@client.event
async def on_ready():
    print("reggie")
    for extension in extensions:
        client.load_extension(extension)

client.run("")