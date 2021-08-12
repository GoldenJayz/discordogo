import discord
from discord.ext import commands
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tmdbsimple as tmbd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="",
    client_secret="")
    )
tmbd.API_KEY = ""
client = discord.Client()

class spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def fetchdata(self, type: str, args: str) -> str:
        data: str = ""
        if type == "artist":
            results = sp.search(q=args, limit=10, type=type)
            for idx, trac in enumerate(results['artists']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "track":
            results = sp.search(q=args, limit=10, type=type)
            for idx, trac in enumerate(results['tracks']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "album":
            results = sp.search(q=args, limit=10, type=type)
            for idx, trac in enumerate(results['albums']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "playlist":
            results = sp.search(q=args, limit=10, type=type)
            for idx, trac in enumerate(results['playlists']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "movie":
            search = tmbd.Search()
            response = search.movie(query=args)
            for s in search.results:
                indexof = search.results.index(s)
                data += f"{indexof + 1}. {s['title']}\n"
        return data

    @commands.command()
    async def search(self, ctx, type: str, *, args: str):
        embed = discord.Embed(
            title="Search API",
            timestamp=datetime.datetime.utcnow(),
            colour=0x00ff08,
            description=await self.fetchdata(type, args)
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @search.error
    async def searcherror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
            title="Spotify Search API",
            timestamp=datetime.datetime.utcnow(),
            colour=0x00ff08,
            description="Example: -spotifysearch track Despacito"
            )
            embed.add_field(name="1st Argument", value="artist|album|track|playlist|movie")
            embed.add_field(name="2nd Argument", value="The search query", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(spotify(client))
