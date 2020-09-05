from discord.ext import commands
from discord import Embed

from random import uniform, randint, choice
from math import floor
from typing import Union
from aiohttp_requests import requests

from cogs.Utility.color import Colors
from cogs.Misc.word import Words
from cogs.Misc.country import Country
from cogs.Misc.image import Images

from scripts.JSON import JSON


class Random(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_random_cat(self):
        cat_api_url = "https://api.thecatapi.com/v1/images/search"
        cat_request = await requests.get(cat_api_url, headers={'x-api-key': "538e943b-b25a-4e8c-8cdf-55e360c630c5"})
        cat_json = dict(await cat_request.json())
        return cat_json[0]['url']

    async def get_random_dog(self):
        dog_api_url = "https://dog.ceo/api/breeds/image/random"
        dog_request = await requests.get(dog_api_url)
        dog_json = dict(await dog_request.json())
        return dog_json['message']

    @commands.group(name="random", help="Rastgele şeyler döndürür.", aliases=["rastgele", "rd"])
    async def random(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.random.commands])))

    @random.command(name="number",
                    help="Belirtilen aralıkta rastgele bir sayı döndürür.",
                    aliases=["num", "sayı"])
    async def number(self, ctx, min_: Union[int, float, str, None],
                     max_: Union[int, float, str, None], floor_=True):
        min_ = min_ if min_ else 0
        max_ = max_ if max_ else 100
        if type(min_) == str:
            new_min = 0
            for letter in min_:
                new_min += ord(letter)
            min_ = new_min
        if type(max_) == str:
            new_max = 0
            for letter in max_:
                new_max += ord(letter)
            max_ = new_max
        random_number = uniform(min_, max_)
        if floor_:
            random_number = floor(random_number)
        await ctx.send("Oluşturduğum rastgele sayı: {0}".format(random_number))

    @random.command(name="cat",
                    help="Rastgele bir kedi fotoğrafı döndürür :3",
                    aliases=["kedi"])
    async def cat(self, ctx):
        await ctx.send(self.get_random_cat())

    @random.command(name="dog",
                    help="Rastgele bir köpek fotoğrafı döndürür :o",
                    aliases=["köpek"])
    async def dog(self, ctx):
        await ctx.send(self.get_random_cat())

    @random.command(name="fact",
                    help="Rastgele bir bilgi döndürür.",
                    aliases=["bilgi"])
    async def fact(self, ctx):
        random_fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"
        fact_request = await requests.get(random_fact_url)
        fact_dict = dict(await fact_request.json())
        fact_embed = Embed().from_dict({
            'title': "Useless Fact",
            'color': 14714208,
            'fields': [
                {
                    'name': fact_dict['text'],
                    'value': "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                }
            ]
        })
        fact_embed.set_footer(text=fact_dict['source_url'])
        await ctx.send(embed=fact_embed)

    @random.command(name="color", help="Rastgele bir renk döndürür.", aliases=["renk"])
    async def color(self, ctx):
        color = "rgb({0}, {1}, {2})".format(randint(0, 255), randint(0, 255), randint(0, 255))
        color_embed = Colors.get_color_embed(color)
        color_file = Colors.get_color_file(color)
        color_embed.set_image(url="attachment://color.png")
        await ctx.send(embed=color_embed, file=color_file)

    @random.command(name="word", help="Rastgele bir kelime döndürür.", aliases=["kelime", "sözcük"])
    async def word(self, ctx):
        random_word_url = "https://wordsapiv1.p.rapidapi.com/words/"
        query_string = {'random': 'true'}
        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "09d5f431f7msh551bf66982331fep1fcccdjsna08b665da14e"
        }
        word_request = await requests.get(random_word_url, params=query_string, headers=headers)
        word_dict = dict(await word_request.json())
        await ctx.send(embed=Words.get_word_embed(word_dict))

    @random.command(name="country",
                    help="Rastgele bir ülke dündürür.",
                    aliases=['ülke'])
    async def country(self, ctx):
        countries = JSON('./json/countries.json').dict['data']
        random_index = randint(0, len(countries))
        selected_country = countries[random_index]
        await ctx.send(embed=Country.get_country_embed(selected_country))

    @random.command(name="sentence",
                    help="Rastgele bir cümle döndürür.",
                    aliases=["cümle"])
    async def sentence(self, ctx, *, should_contain=" "):
        sentences = JSON('./json/sentences.json').dict['data']
        sentences = list(filter(lambda sentence_: should_contain.lower() in str(sentence_).lower(), sentences))
        if not sentences:
            await ctx.send("'{}' kelimesini içeren bir cümle bulunamadı :|".format(should_contain))
            return False
        await ctx.send(choice(sentences)['sentence'])

    @random.command(name="image", help="Rastgele bir fotoğraf döndürür.", aliases=["fotoğraf", "resim"])
    async def image(self, ctx):
        url = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {JSON('json/auth.json').dict.get('unsplash').get('access-key')}"}
        request = await requests.get(url, headers=headers)
        image_dict = dict(await request.json())
        await ctx.send(embed=Images.get_image_embed(image_dict))

    @commands.command(name="cat", help="Rastgele bir kedi döndürür.", aliases=["kedi"])
    async def randomcat(self, ctx):
        await ctx.send(self.get_random_cat())

    @commands.command(name="dog", help="Rastgele bir köpek döndürür.", aliases=["köpek"])
    async def randomdog(self, ctx):
        await ctx.send(self.get_random_dog())


def setup(client):
    client.add_cog(Random(client))
