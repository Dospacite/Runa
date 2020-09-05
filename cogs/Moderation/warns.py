from discord import Member
from discord.ext import commands
from scripts.checks import is_helper
from scripts.language import TR
from scripts.utility import fetch_from_server


class Warns(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='warn',
                      help="Bir kullanıcıya ikaz verir.",
                      aliases=['ikaz', 'uyar', 'uyarı'])
    @is_helper()
    @commands.guild_only()
    async def warn(self, ctx, member: Member, *, reason: str = None):
        if member.id \
                not in [tpl[0] for tpl in await fetch_from_server(ctx.guild.id, "SELECT MemberID FROM Members")]:
            await fetch_from_server(ctx.guild.id, f"INSERT INTO Members VALUES ({member.id}, 1)")
        else:
            await fetch_from_server(ctx.guild.id,
                                    f"UPDATE Members SET Warnings = Warnings + 1 WHERE MemberID = {member.id}")
        await ctx.send("{0}, {1} tarafından, {2} sebebiyle uyarıldı. Bu onun {3}. uyarısı."
                       .format(member.mention,
                               ctx.author.mention,
                               reason,
                               (await fetch_from_server(
                                   ctx.guild.id,
                                   f"SELECT Warnings FROM Members WHERE MemberID = {member.id}"))[0][0]))

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(TR().dict.get('NO_MEMBER'))

    @commands.command(name='unwarn', help="Kullanıcının ikazlarından birini kaldırır.", aliases=['ikazçek', 'uyarma'])
    @is_helper()
    @commands.guild_only()
    async def unwarn(self, ctx, *, member: Member):
        if member.id \
                not in [tpl[0] for tpl in await fetch_from_server(ctx.guild.id, "SELECT MemberID FROM Members")]:
            await fetch_from_server(ctx.guild.id, f"INSERT INTO Members VALUES ({member.id}, 0)")
        else:
            await fetch_from_server(ctx.guild.id,
                                    f"UPDATE Members SET Warnings = Warnings - 1 WHERE MemberID = {member.id}")
        if await fetch_from_server(ctx.guild.id, f"SELECT Warnings FROM Members WHERE MemberID = {member.id}"):
            await fetch_from_server(ctx.guild.id,
                                    f"UPDATE Members SET Warnings = 0 WHERE MemberID = {member.id}")
        await ctx.send("{0}'nın bir uyarısı {1} tarafından kaldırıldı. {2} uyarısı kaldı."
                       .format(member.mention,
                               ctx.author.mention,
                               (await fetch_from_server(
                                   ctx.guild.id,
                                   f"SELECT Warnings FROM Members WHERE MemberID = {member.id}"))[0][0]))

    @unwarn.error
    async def unwarn_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(TR().dict.get('NO_MEMBER'))

    @commands.command(name="warnings", help="Kullanıcının ikazlarını görüntüler.", aliases=['uyarılar', 'warns'])
    @is_helper()
    @commands.guild_only()
    async def warnings(self, ctx, *, member: Member):
        member_warnings = (await fetch_from_server(ctx.guild.id,
                                                   f"SELECT Warnings FROM Members WHERE MemberID = {member.id}"))
        member_warnings = member_warnings[0][0] if member_warnings else 0
        await ctx.send("{0}'nin ikaz sayısı {1} :|".format(member.mention, member_warnings))

    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(TR().dict.get('NO_MEMBER'))


def setup(client):
    client.add_cog(Warns(client))
