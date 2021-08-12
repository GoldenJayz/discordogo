import discord
from discord.ext import commands
import datetime
import json
from PIL import Image
from io import BytesIO

client = discord.Client()
prefix: str = ""
AmongUsMode: bool = False

class meme(commands.Cog):
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
            for data in jason:
                if data == str(guildid):
                    return jason[str(guildid)][0]["AmongUsMode"]

    """
    @commands.command()
    async def setup(self, ctx):
        print("hi")
    """

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        global prefix
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                with open("./cogs/guildconfig.json") as jasonlel:
                    jason = json.load(jasonlel)
                for guildid in jason:
                    print(guildid)

                await channel.send(
                    "Hello, thanks for inviting me into your Guild! I need to ask a couple of questions first."
                )
                await channel.send(
                    "Would you like to enable among us mode (replies to messages that contain sus)?"
                )
                print(self.client.user)
                msg = await self.client.wait_for("message")
                await channel.send("What would you like the bot prefix?")
                botprefixques = await self.client.wait_for("message")
                responses = [msg, botprefixques]
                global AmongUsMode
                if msg.content.lower() == "yes":
                    print("here")
                    AmongUsMode = True
                    if responses[1].content.lower:
                        prefix = responses[1].content
                elif msg.content.lower() == "no":
                    print("chez")
                    AmongUsMode = False
                    if responses[1].content.lower:
                        prefix = responses[1].content
                
                jason["Guilds"].update({f"{guild.id}": {"prefix": prefix, "amongus": AmongUsMode}})

                print(jason)
                with open("./cogs/guildconfig.json", "w") as sup_jason_file:
                    json.dump(jason, sup_jason_file)
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
    client.add_cog(meme(client))

"""
    Async function to load the guild configuration file
    1. load prefix from guild configuration file
    2. turn it into a command

"""
