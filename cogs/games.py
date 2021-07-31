import discord
from discord.ext import commands
import random
import datetime
from PIL import Image
from io import BytesIO

client = discord.Client()

class games(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def editimage(self, embed, author, target):
        IMAGE = Image.open("heart.jpg")
        AUTHOR_PFP = author.avatar_url_as(size=256)
        TARGET_PFP = target.avatar_url_as(size=256)
        AUTHOR_DATA = BytesIO(await AUTHOR_PFP.read())
        TARGET_DATA = BytesIO(await TARGET_PFP.read())
        APFP = Image.open(AUTHOR_DATA)
        APFP = APFP.resize((354,354))
        TPFP = Image.open(TARGET_DATA)
        TPFP = TPFP.resize((354,354))
        IMAGE.paste(TPFP, (800,212))
        IMAGE.save("profile.jpg")
        IMAGE.paste(APFP, (120,212))
        IMAGE.save("profile.jpg")

    async def lovemaker(self, ctx, embed, member):
        resultint: int = random.randrange(0,11)
        stringed_result: str = ""
        EMOJI: str = "<:redbar:870829592326316052>"
        BLANK_EMOJI: str = "<:blackbar:870829932304007168>"
        for i in range(resultint):
            stringed_result += EMOJI
            if i == resultint-1:
                blank_emojis: int = 11 - resultint
                for x in range(blank_emojis):
                    stringed_result += BLANK_EMOJI
        if resultint == 0:
            for i in range(10):
                stringed_result += BLANK_EMOJI
            embed.add_field(name=f"{ctx.author} <3 {member}", value=f"{resultint}% {stringed_result} RIP")
        else:
            embed.add_field(name=f"{ctx.author} <3 {member}", value=f"{resultint}0% {stringed_result}")

        #show all black bars if 0
    
    @commands.command()
    async def love(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=0xd09adf)
        file = discord.File("profile.jpg", filename="profile.jpg")
        embed.set_image(url="attachment://profile.jpg")
        author = ctx.author
        await self.lovemaker(ctx, embed, member)
        await self.editimage(embed, author, member)
        await ctx.send(file=file, embed=embed)

def setup(client):
    client.add_cog(games(client))

# make it add both users pfp
# encode the image
# if the member is nora make love 100% lol
# error handling