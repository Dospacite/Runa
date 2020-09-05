from discord.ext import commands
from discord import Role
from scripts.checks import is_admin
from scripts.utility import fetch_from_server
from scripts.language import TR


class Roles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    async def staffrole(staff: str, ctx: commands.Context, role: Role = None):
        """

        :param staff: Staff role this function will be used for. Can be 'Admin', 'Mod', 'Helper'
        :param ctx: Context that was passed during command invocation
        :param role: Role that the staff role will be set to. If it's None, staff role will be displayed.
        :return: True if 'role' was not passed
        """
        staff = staff.title()
        if not role:
            role = ctx.guild.get_role((await fetch_from_server(ctx.guild.id, f"SELECT {staff}RoleID FROM Meta"))[0][0])
            await ctx.send("{0} rolü: {1}".format(staff, role.mention if role else "Yok :|"))
            return True
        else:
            await fetch_from_server(ctx.guild.id, f"UPDATE Meta SET {staff}RoleID = {role.id}")
            await ctx.send("{0} rolü {1} olarak ayarlandı :|".format(staff, role.mention))

    @commands.command(name="adminrole", help="Admin rolünü ayarlar.")
    @is_admin()
    @commands.guild_only()
    async def adminrole(self, ctx, role: Role = None):
        await Roles.staffrole("admin", ctx, role)

    @adminrole.error
    async def adminrole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('ARGUMENT_NOT_ROLE'))

    @commands.command(name="modrole", help="Moderatör rolünü ayarlar.")
    @is_admin()
    @commands.guild_only()
    async def modrole(self, ctx, role: Role = None):
        await Roles.staffrole("mod", ctx, role)

    @modrole.error
    async def modrole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('ARGUMENT_NOT_ROLE'))

    @commands.command(name="helperrole", help="Yardımcı rolünü ayarlar.")
    @is_admin()
    @commands.guild_only()
    async def helperrole(self, ctx, role: Role = None):
        await Roles.staffrole("helper", ctx, role)

    @helperrole.error
    async def helperrole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('ARGUMENT_NOT_ROLE'))


def setup(client):
    client.add_cog(Roles(client))
