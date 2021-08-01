import discord
from discord.ext import commands
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="",
    client_secret="")
    )
client = discord.Client()

class spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def fetchdata(self, type: str, args: str) -> str:
        data: str = ""
        results = sp.search(q=args, limit=10, type=type)
        if type == "artist":
            for idx, trac in enumerate(results['artists']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "track":
            for idx, trac in enumerate(results['tracks']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "album":
            for idx, trac in enumerate(results['albums']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "playlist":
            for idx, trac in enumerate(results['playlists']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        return data

    @commands.command()
    async def spotifysearch(self, ctx, type: str, *, args: str):
        embed = discord.Embed(
            title="Spotify Search API",
            timestamp=datetime.datetime.utcnow(),
            colour=0x00ff08,
            description=await self.fetchdata(type, args)
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @spotifysearch.error
    async def spotifyerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
            title="Spotify Search API",
            timestamp=datetime.datetime.utcnow(),
            colour=0x00ff08,
            description="Example: -spotifysearch track Despacito"
            )
            embed.add_field(name="1st Argument", value="artist|album|track|playlist")
            embed.add_field(name="2nd Arguement", value="The search query", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(spotify(client))