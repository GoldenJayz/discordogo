import discord
from discord.ext import commands
import json

client = discord.Client()

extensions = {
    "cogs.spotify",
    "cogs.games",
    "cogs._setup",
    "cogs.config"
}

def get_prefix(client, message) -> str:
    with open("./cogs/guildconfig.json") as jason:
        joemama = json.load(jason)
    return str(joemama["Guilds"][0][f"{message.guild.id}"]["prefix"])

client = commands.Bot(command_prefix=(get_prefix))

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

client.run("")
