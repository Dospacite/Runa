from discord import Member
from discord.ext import commands
from discord.utils import find

from scripts.checks import is_mod
from scripts.language import TR


class Bans(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='ban',
                      help='Kullanıcıyı sunucudan yasaklar.')
    @is_mod()
    @commands.guild_only()
    async def ban(self, ctx, member: Member = None, reason: str = None):
        await ctx.send('Kullanıcı {0}, {1} sebebiyle, {2} tarafından yasaklandı :O'
                       .format(member.mention, reason, ctx.author.mention))
        await ctx.guild.ban(member, reason=reason if reason else None)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(TR().dict.get('NO_PERMISSION'))
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))

    @commands.command(name="unban",
                      help="Kullanıcının yasağını kaldırır.")
    @commands.guild_only()
    @is_mod()
    async def unban(self, ctx, user):
        entry = find(lambda ban_entry: ban_entry.user.name.lower() == user.lower(), await ctx.guild.bans())
        if not entry:
            raise commands.BadArgument
        await ctx.guild.unban(entry.user)
        await ctx.send("{0}'nın yasağı, {1} tarafından kaldırıldı :|".format(user.name, ctx.author.mention))

    @unban.error
    async def unban_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CheckFailure):
            await ctx.send(TR().dict.get('NO_PERMISSION'))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(TR().dict.get('NO_MEMBER'))
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))


def setup(client):
    client.add_cog(Bans(client))
