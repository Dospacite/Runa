from discord.ext import commands
from typing import Union
from scripts.JSON import JSON
from scripts.language import TR


class Convert(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='convert',
                      help='Tipler arası dönüşüm yapar.')
    async def convert(self, ctx, value: Union[float, int, None], conversion: str):
        conversion_embed = JSON('../../embeds/conversions.json')
        answer = str()
        if not conversion:
            await ctx.send(TR().dict.get('NO_CONVERSION'))
            await ctx.send(embed=conversion_embed)
            return False
        if not value:
            await ctx.send(TR().dict.get('NO_CONVERSION_VALUE'))
            await ctx.send(embed=conversion_embed)
            return False
        async with ctx.typing():
            if conversion.lower() == 'ctof':
                answer = value * 1.8 + 32
            elif conversion.lower() == 'ftoc':
                answer = (value - 32) / 1.8

            elif conversion.lower() == 'milestokm':
                answer = value / 0.62137
            elif conversion.lower() == 'kmtomiles':
                answer = value * 0.62137

            elif conversion.lower() == 'kgtolb':
                answer = value * 2.2046
            elif conversion.lower() == 'lbtokg':
                answer = value / 2.2046

            elif conversion.lower() == 'fttom':
                answer = value / 3.2808
            elif conversion.lower() == 'mtoft':
                answer = value * 3.2808

            elif conversion.lower() == 'intocm':
                answer = value / 0.39370
            elif conversion.lower() == 'cmtoin':
                answer = value * 0.39370

            else:
                await ctx.send(embed=conversion_embed)
        if answer:
            await ctx.send(str(answer))
        return True


def setup(client):
    client.add_cog(Convert(client))
