import discord
from discord.ext import commands
import json

client = discord.Client()

extensions = {
    "cogs.spotify",
    "cogs.games",
    "cogs.meme"
}

class setup():
    def __init__(self, guildid):
        self.fetch_prefix(guildid)
    
    async def fetch_prefix(self, guildid):
        with open("./cogs/guildconfig.json", "w") as jason:
            joemama = json.load(jason)
        for guild in joemama["Guilds"]:
            print(guild)

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"))

@client.event
async def on_ready():
    print("reggie")
    for extension in extensions:
        client.load_extension(extension)

@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} is disabled.')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("The bot is missing permissions.")

@client.command()
@has_permissions(administrator=True)
async def setup(ctx):
    

# get prefix from guild config file


client.run("")
