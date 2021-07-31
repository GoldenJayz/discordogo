import discord
from discord.ext import tasks, commands
import datetime
import asyncio


client = discord.Client()


class spotify(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(spotify(client))