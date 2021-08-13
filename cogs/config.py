import discord
from discord.ext import commands
import json

client = discord.Client()

class config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setup(self, ctx):
        def check(x):
            return x.author.id == ctx.author.id
            
        await ctx.send("Would you like to enable among us mode?")
        response = await self.client.wait_for("message", check=check)
        with open("./cogs/guildconfig.json") as jasonfile:
            jason = json.load(jasonfile)
        if response.content == "yes":
            jason["Guilds"][0][f"{ctx.guild.id}"]["Among"] = True
        await ctx.send("Would you like to change the prefix?")
        prefixques = await self.client.wait_for("message", check=check)
        if prefixques.content == "yes":
            await ctx.send("Please send what you wish the new prefix to be.")
            newprefix = await self.client.wait_for("message", check=check)
            jason["Guilds"][0][f"{ctx.guild.id}"]["prefix"] = newprefix.content
        else:
            print(prefixques.content)
            jason["Guilds"][0][f"{ctx.guild.id}"]["prefix"] = "-"
        with open("./cogs/guildconfig.json", "w") as bruh:
            json.dump(jason, bruh)


def setup(client):
    client.add_cog(config(client))
