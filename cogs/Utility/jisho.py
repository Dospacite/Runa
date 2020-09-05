from discord.ext import commands
from discord import Embed
from aiohttp_requests import requests


class Jisho(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_jp_embed(self, jp_dict):
        word = jp_dict.get('japanese')[0]['word'] \
            if jp_dict.get('japanese')[0].get('word') \
            else jp_dict.get('japanese')[0]['reading']
        embed = Embed().from_dict({
            'title': f"{word} - {jp_dict.get('japanese')[0]['reading']}",
            'color': 14714208,
            'description': f"Anlamı: {', '.join(jp_dict.get('senses')[0]['english_definitions'])}\n"
                           f"Kullanım Yeri: {jp_dict.get('senses')[0]['parts_of_speech'][0]}"

        })
        return embed

    @commands.command(name="jisho",
                      help="Jisho'dan bir japonca kelime veya kanji döndürür.",
                      aliases=["jp"])
    async def jisho(self, ctx, *, string):
        index = string[-1]
        try:
            index = int(index)
            string = string[:-2]
        except ValueError:
            index = 1
        url = f"https://jisho.org/api/v1/search/words?keyword={string}"
        request = await requests.get(url)
        request_dict = dict(await request.json())
        if not request_dict.get('data'):
            await ctx.send("Kelime bulunamadı :|")
            return False
        await ctx.send(embed=await self.get_jp_embed(request_dict['data'][index-1]))


def setup(client):
    client.add_cog(Jisho(client))
