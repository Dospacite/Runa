from discord.ext import commands
from discord import TextChannel
from typing import Optional
from scripts.checks import is_mod
from scripts.language import TR


class Channel(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='slowmode', help="Kanala yavaş mod ekler.")
    @is_mod()
    async def slowmode(self, ctx, seconds: Optional[int], channel: Optional[TextChannel]):
        if not seconds:
            seconds = 0
        if not channel:
            channel = ctx.channel
        await channel.edit(reason="{0} initiated slowmode."
                           .format(ctx.author.name), slowmode_delay=seconds)
        if seconds:
            await channel.send("{0} bu kanalda yavaş modu etkinleştirdi :|"
                               .format(ctx.author.mention))
        else:
            await channel.send("{0} bu kanalda yavaş modu kaldırdı :|"
                               .format(ctx.author.mention))

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(TR().dict.get('NO_PERMISSION'))


def setup(client):
    client.add_cog(Channel(client))
