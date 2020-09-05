from discord.ext import commands
from discord import VoiceChannel, Client


class Voice(commands.Cog):

    def __init__(self, client: Client):
        self.client = client

    @commands.group(name="voice", help="Ses ile ilgili komutları barındırır.", aliases=["ses"])
    @commands.guild_only()
    async def voice(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.voice.commands])))

    @voice.command(name="join", help="Ses kanalına bağlanır", aliases=["katıl"])
    async def join(self, ctx: commands.Context, channel: VoiceChannel = None):
        if not channel:
            channel = ctx.author.voice.channel
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        await channel.connect()

    @join.error
    async def join_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Bir ses kanalında değilsin :|")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Ses kanalı bulunamadı :|")

    @voice.command(name="leave", help="Ses kanalından ayrılır.", aliases=["ayrıl"])
    async def leave(self, ctx: commands.Context):
        await ctx.guild.voice_client.disconnect()

    @leave.error
    async def leave_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Bir ses kanalında değilim :|")


def setup(client):
    client.add_cog(Voice(client))
