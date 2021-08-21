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
        spotifytypes = ["artist", "track", "album", "playlist"]
        if type in spotifytypes:
            results = sp.search(q=args, limit=10, type=type)
            for idx, trac in enumerate(results[f'{type}s']['items']):
                data += f"{idx + 1}. {trac['name']}\n"
        elif type == "movie":
            search = tmbd.Search()
            response = search.movie(query=args)
            for s in search.results:
                indexof = search.results.index(s)
                data += f"{indexof + 1}. {s['title']}\n"
        return data

    async def categorize(self, type: str, trac) -> str:
        if type == "album":
            return f"{trac['name']}\n{trac['release_date']}\n{trac['total_tracks']}"
        elif type =="track":
            return f"**Track Name: **{trac['name']}\n**Preview Url: **{trac['preview_url']}\n**ID:** {trac['id']}\n**Popularity: ** {trac['popularity']}"
        elif type =="playlist":
            return f"**Playlist Name: **{trac['name']}\n**Playlist Owner: **{trac['owner']['display_name']}\n**Public: **{trac['public']}\n**Tracks: **{trac['tracks']['total']}\n**Collaborative: **{trac['collaborative']}\n**Description: **{trac['description']}\n**Playlist Link: **{trac['external_urls']['spotify']}\n**ID: **{trac['id']}\n"
        elif type =="artist":
            return f"**Artist Name: **{trac['name']}"
    
    @commands.command()
    async def search(self, ctx, type: str, *, args: str):
        if await self.fetchdata(type, args) == "":
            await ctx.send("Please provide a valid search type!")
        else:
            embed = discord.Embed(
                title="Search API",
                timestamp=datetime.datetime.utcnow(),
                colour=0x00ff08,
                description=await self.fetchdata(type, args)
            )
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)
            index = await self.client.wait_for("message")
            results = sp.search(q=args, limit=10, type=type)
            if index.content in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                for idx, trac in enumerate(results[f'{type}s']['items']):
                    if int(index.content) == idx + 1:
                        embed = discord.Embed(
                            title=f"{trac['name']} Data",
                            timestamp=datetime.datetime.utcnow(),
                            description=await self.categorize(type, trac),
                            colour=0x00ff08
                            )
                        await ctx.send(embed=embed)
                        break

    @search.error
    async def searcherror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Search Command",
                timestamp=datetime.datetime.utcnow(),
                colour=0x00ff08
            )
            embed.add_field(name="Argument 1", value="artist | album | track | playlist | movie")
            embed.add_field(name="Argument 2", value="<search query>", inline=False)
            embed.set_image(url="https://cdn.discordapp.com/attachments/742148980682784793/875745757418885160/unknown.png")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(spotify(client))
