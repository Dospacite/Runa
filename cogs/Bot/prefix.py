from discord.ext import commands
from scripts.utility import fetch_from_server
from scripts.checks import is_admin


class Prefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="prefix", help="Sunucu için Runa'nın prefixini değiştirir.")
    @is_admin()
    async def prefix(self, ctx, value=None):
        if not value:
            server_prefix = (await fetch_from_server(ctx.guild.id,
                                                     "SELECT Prefix FROM Meta"))[0][0]
            await ctx.send("Sunucu içi prefixim: `{0}`".format(server_prefix))
            return True
        if len(value) > 5:
            await ctx.send("Prefix 5 karakterden uzun olamaz :|")
            return False
        await fetch_from_server(ctx.guild.id,
                                f"UPDATE Meta SET Prefix = '{value}'")
        await ctx.send("Sunucu içi prefixim `{0}` olarak değiştirildi :|".format(value))


def setup(client):
    client.add_cog(Prefix(client))
