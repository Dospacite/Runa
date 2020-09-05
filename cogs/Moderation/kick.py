from discord import Member
from discord.ext import commands
from scripts.checks import is_mod, is_admin
from scripts.language import TR


class Kicks(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='kick',
                      help='Kullanıcıyı sunucudan atar.')
    @is_mod()
    @commands.guild_only()
    async def kick(self, ctx, member: Member = None, reason: str = None):
        await ctx.send('Kullanıcı {0}, {1} sebebiyle, {2} tarafından atıldı :O'
                       .format(member.mention, reason, ctx.author.mention))
        await ctx.guild.kick(member, reason=reason if reason else None)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))


def setup(client):
    client.add_cog(Kicks(client))
