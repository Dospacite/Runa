from discord.ext import commands
from scripts.checks import is_mod


class Channel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='prune', help="Belirtilen sayı kadar mesaj siler.")
    @commands.guild_only()
    @is_mod()
    async def prune(self, ctx, message_count: int = 100):
        """
        Prune (runa prune [message_count]) is a command that deletes the specified amount of messages (message_count)
        from the channel the command was called from.
        Command needs to be executed in a guild.
        Command executor needs to have manage_messages permission in that channel.
        :param ctx: discord.Context, passed by default.
        :param message_count: total number of messages that will be deleted, limited to 100
        :return: True if no error was raised
        """
        message_count = 100 if message_count > 100 else message_count  # Limiting message_count for Discord API
        async with ctx.typing():
            marked_messages = await ctx.channel.history(limit=message_count).flatten()
            await ctx.channel.delete_messages(marked_messages)
        await ctx.send(f"{len(marked_messages)} mesaj silindi :|", delete_after=2.0)

    @prune.error
    async def prune_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Silinecek mesajlar arasında 14 günden daha eski mesajlar bulunamaz :|")


def setup(client):
    client.add_cog(Channel(client))
