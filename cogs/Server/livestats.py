from discord.ext import commands
from scripts.utility import fetch_from_server
from scripts.checks import is_admin


class Livestats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(name="livestats",
                    help="Sunucu içindeki bilgileri canlı olarak gösteren bir ses kanalı açar.",
                    aliases=["canlısayaç", "livecount"])
    async def livestats(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.livestats.commands])))

    @livestats.command(name="member",
                       help="Sunucudaki kullanıcı sayısını gösteren bir ses kanalı açar.",
                       aliases=["üye", "membercount"])
    @commands.guild_only()
    @is_admin()
    async def membercount(self, ctx: commands.Context, option=None):
        """
        Creates a voice channel that displays a live member count.
        This count is then modified when the bot is ready or when a member joins or leaves.
        :param ctx: Context that was passed on call
        :param option: What to do with the channel. Can be "create" or "remove"
        :return: Nothing
        """
        if not option or option.lower() == "create":
            # If guild already has a livecount channel,
            if (await fetch_from_server(ctx.guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0]:
                # Send confirmation message and the channel in rapid succession.
                await ctx.send("Kullanıcı sayısını bir kanal zaten gösteriyor :|")
                await ctx.send(ctx.guild.get_channel((await fetch_from_server(ctx.guild.id,
                                                                              """SELECT MembercountChannelID
                                                                                 FROM Meta"""))[0][0]))
            else:  # If guild does not have a initalized
                # Create the voice channel
                channel = await ctx.guild.create_voice_channel("Kullanıcı Sayısı: {}".format(len(ctx.guild.members)))
                # Create livecount entry in the database
                await fetch_from_server(ctx.guild.id, f"UPDATE Meta SET MembercountChannelID = {channel.id}")
                # Send confirmation message
                await ctx.send("Kullanıcı sayısını gösteren kanalı açtım :|")

        elif option == "remove":
            # If guild does not have a livecount channel,
            if not (await fetch_from_server(ctx.guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0]:
                # Send confirmation message
                await ctx.send("Kullanıcı sayısını gösteren bir kanal yok :|")
            else:  # If guild does have a livecount channel,
                # Get the channel from the database
                channel = ctx.guild.get_channel(
                    (await fetch_from_server(ctx.guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0])
                # Delete the channel
                await channel.delete()
                # Update the database, setting livecount channel to None
                await fetch_from_server(ctx.guild.id, f"UPDATE Meta SET MembercountChannelID = NULL")
                # Send the confirmation message
                await ctx.send("Kullanıcı sayısını gösteren kanal kaldırıldı :|")


def setup(client):
    client.add_cog(Livestats(client))
