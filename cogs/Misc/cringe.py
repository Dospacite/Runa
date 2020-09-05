from discord.ext.commands import Cog, command
from discord import File, Member
from typing import Optional
from os import listdir
from random import randint


class Cringe(Cog):
    def __init__(self, client):
        self.client = client

    @command(name='cringe', help='You posted cringe', aliases=['cring', 'crong', 'cirng'])
    async def cringe(self, ctx, *, member: Optional[Member]):
        files = listdir('images/cringe')
        filename = files[randint(0, len(files))]
        await ctx.send(member.mention if member else None, file=File('images/cringe/' + filename))


def setup(client):
    client.add_cog(Cringe(client))
