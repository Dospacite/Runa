from discord import Member
from discord.ext import commands
from scripts.checks import is_helper, is_mod, is_admin
from scripts.language import TR


class Mutes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='mute', help="Bir kullanıcıyı susturur.")
    @commands.guild_only()
    @is_helper()
    async def mute(self, ctx, member: Member, reason=None):
        async with ctx.typing():
            for channel in ctx.guild.channels:
                await channel.set_permissions(member, send_messages=False)
        await ctx.send("{0} {1} tarafından {2} sebebiyle susturuldu :|"
                       .format(member.mention, ctx.author.mention, reason if reason else "'Belirtilmemiş'"))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(TR().dict.get('NO_PERMISSION'))
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))

    @commands.command(name='unmute', help="Kullanıcının susturmasını kaldırır.")
    @commands.guild_only()
    @is_helper()
    async def unmute(self, ctx, member: Member):
        async with ctx.typing():
            for channel in ctx.guild.channels:
                if not channel.permissions_for(member).send_messages:
                    await channel.set_permissions(member, overwrite=None)
            await ctx.send("{0}' susturması {1} tarafından kaldırıldı :|"
                           .format(member.mention, ctx.author.mention))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(TR().dict.get('NO_PERMISSION'))
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('MEMBER_NOT_FOUND'))


def setup(client):
    client.add_cog(Mutes(client))
