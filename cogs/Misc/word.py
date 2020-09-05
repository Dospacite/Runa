from discord.ext import commands
from discord import Embed
from aiohttp_requests import requests


class Words(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_word_embed(word_dict):
        word_embed = Embed().from_dict({
            'title': word_dict.get('word').title(),
            'color': 1000000,
        })
        has_results = word_dict.get('results')
        if not has_results:
            word_embed.set_footer(text="Anlamı bulunamadı :|")
            return word_embed
        for n, definition in enumerate(word_dict.get('results')):
            word_embed.add_field(name=f"Anlam {n+1}",
                                 value=definition.get('definition').capitalize() + ".",
                                 inline=False)
        return word_embed

    @commands.command(name="randomword",
                      help="Rastgele bir kelime döndürür.",
                      aliases=["rastgelekelime", "rastgelesözcük"])
    async def randomword(self, ctx):
        random_word_url = "https://wordsapiv1.p.rapidapi.com/words/"
        query_string = {'random': 'true'}
        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "09d5f431f7msh551bf66982331fep1fcccdjsna08b665da14e"
        }
        word_request = requests.get(random_word_url, params=query_string, headers=headers)
        word_dict = dict(await word_request.json())
        await ctx.send(embed=Words.get_word_embed(word_dict))

    @commands.command(name="word",
                      help="Belirtilen kelimeyi döndürür.",
                      aliases=["kelime", "sözcük"])
    async def word(self, ctx, *, word):
        if not word or word.lower() == "random":
            await self.randomword()
            return True
        random_word_url = "https://wordsapiv1.p.rapidapi.com/words/{}"
        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "09d5f431f7msh551bf66982331fep1fcccdjsna08b665da14e"
        }
        word_request = await requests.get(random_word_url.format(word), headers=headers)
        word_dict = dict(await word_request.json())
        await ctx.send(embed=self.get_word_embed(word_dict))

    @word.error
    async def word_error(self, ctx, error):
        print(error)
        if isinstance(error, TypeError):
            await ctx.send("Kelime bulunamadı :|")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Bir kelime belirtmediniz :|")


def setup(client):
    client.add_cog(Words(client))
