from discord.ext import commands
from discord import Embed
from aiohttp_requests import requests
from scripts.JSON import JSON


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_image_embed(image_dict):
        image_embed = Embed().from_dict({
            "title": f"Image {image_dict.get('id')}",
            "color": int(image_dict.get('color')[1:], 16),
            "description": image_dict.get('description')
        })
        image_embed.set_image(url=image_dict.get('urls').get('full'))
        image_embed.set_footer(text=f"Shot by {image_dict.get('user').get('name')}\n"
                                    f"Author Link: {image_dict.get('user').get('links').get('html')}\n"
                                    f"Image Link: {image_dict.get('urls').get('full')}")
        return image_embed

    @commands.command(name="image",
                      help="Belirtilen arama ile ilgili bir fotoğraf döndürür.",
                      aliases=["resim", "fotoğraf"])
    async def image(self, ctx, keyword: str):
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {JSON('json/auth.json').dict.get('unsplash').get('access-key')}"}
        query = {'query': keyword}
        request = await requests.get(url, headers=headers, params=query)
        request_dict = dict(await request.json())
        await ctx.send(embed=Images.get_image_embed(request_dict.get('results')[0]))


def setup(client):
    client.add_cog(Images(client))
