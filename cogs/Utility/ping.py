from discord.ext import commands
from math import ceil


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='ping',
                      help="Runa'nın Discord sunucuları ile arasındaki gecikmeyi gösterir.",
                      aliases=['gecikme'])
    async def ping(self, ctx):
        await ctx.send("Pong! Gecikmem {0}ms!".format(ceil(self.client.latency)))


def setup(client):
    client.add_cog(Ping(client))
