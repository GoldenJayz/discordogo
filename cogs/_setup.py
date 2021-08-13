import discord
from discord.ext import commands
import datetime
import json
from PIL import Image
from io import BytesIO

client = discord.Client()

class _setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def editimage(self, target):
        IMAGE = Image.open("amoogus.jpg")
        TARGET_PFP = target.avatar_url_as(size=128)
        TARGET_DATA = BytesIO(await TARGET_PFP.read())
        TPFP = Image.open(TARGET_DATA)
        TPFP = TPFP.resize((110, 110))
        TPFP = TPFP.convert("RGB")
        IMAGE = IMAGE.convert("RGB")
        IMAGE.paste(TPFP, (150, 84))
        IMAGE.save("sus.jpg")

    async def load_guild_config(self, guildid: int) -> bool:
        with open("./cogs/guildconfig.json") as jasonfile:
            jason = json.load(jasonfile)
            for data in jason["Guilds"]:
                if data[f"{guildid}"]:
                    return jason["Guilds"][0][f"{guildid}"]["Among"]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("./cogs/guildconfig.json") as jasonfile:
            jason = json.load(jasonfile)
        jason["Guilds"][0].update({f"{guild.id}": {"prefix": "-", "Among": False}})
        with open("./cogs/guildconfig.json", "w") as jasonfile:
            json.dump(jason, jasonfile)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Thank you for inviting me into your server! You can change my configuration by doing ```-setup```")
            break

    @commands.Cog.listener()
    async def on_message(self, msg):
        result = await self.load_guild_config(msg.guild.id)
        if msg.author == self.client.user:
            return
        else:
            if result == True:
                if "sus" in msg.content:
                    await self.editimage(msg.author)
                    file = discord.File("sus.jpg", filename="sus.jpg")
                    await msg.channel.send("impostor?", file=file)


def setup(client):
    client.add_cog(_setup(client))
