from discord.ext import commands
from discord import Embed
from discord.utils import find
from scripts.JSON import JSON
from random import choice


class Country(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_country_embed(country):
        country_languages = []
        for language in country['languages']:
            country_languages.append(language['name'])
        country_embed = Embed().from_dict({
            'title': str(country['name']),
            'color': 14714208,
            'fields': [
                {  # Capital
                    "name": 'Başkent',
                    "value": str(country['capital']),
                    "inline": False
                },
                {  # Population
                    "name": 'Nüfus',
                    "value": str(country['population']),
                    "inline": False
                },
                {  # Region
                    "name": 'Bölge',
                    "value": str(country['subregion']),
                    "inline": False
                },
                {  # Timezone
                    "name": 'Zaman Dilimi',
                    "value": str(country['timezones'][0]),
                    "inline": False
                },
                {  # Area
                    "name": 'Yüzey Alanı',
                    "value": f"{str(country['area'])} Kilometre Kare",
                    "inline": False
                },
                {  # Languages
                    "name": 'Konuşulan Diller',
                    "value": str(", ".join(country_languages)),
                    "inline": False
                },
                {  # Flag URL
                    "name": "Bayrak URL'i",
                    "value": str(country['flag']),
                    "inline": False
                }
            ]
        })
        country_embed.set_image(url="http://www.geognos.com/api/en/countries/flag/{}.png".format(country['alpha2Code']))
        return country_embed

    @commands.command(name="country",
                      help="Belirtilen ülkeyi dündürür.",
                      aliases=['ülke', 'get_country', 'getcountry'])
    async def get_country(self, ctx, *, country=None):
        countries = JSON('./json/countries.json').dict['data']
        if not country or country.lower() == "random":
            country = choice(countries)
        else:
            country = find(lambda country_: country.lower() in str(country_).lower(), countries)
        await ctx.send(embed=self.get_country_embed(country))


def setup(client):
    client.add_cog(Country(client))
