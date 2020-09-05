from discord.ext import commands
from discord import Role, Embed
from scripts.utility import fetch_from_server
from scripts.checks import is_mod


class ReactionRoles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(name="reactionroles",
                    help="Reaksiyon üzerine rol vermeyi sağlayan mesajları oluşturmayı sağlar.",
                    aliases=["reaksiyonrolleri", "reactionrole", "reaksiyonrol", "reactrole"])
    async def reactionroles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.reactionroles.commands])))

    @reactionroles.command()
    @is_mod()
    @commands.guild_only()
    async def create(self, ctx: commands.Context, role: Role, emoji: str, *, content=None):
        """
        Creates a ReactionRole that gives the specified role to the user upon reacting to the message.
        This function is corrolated with 'on_raw_reaction_add' and 'on_raw_reaction_remove' in 'guild_listeners.py'
        :param ctx: Context that was passed during command invocation.
        :param role: Role that will be given to users upon reaction.
        :param emoji: Emoji that will be pre-added to the embed message. Purely cosmetic.
        :param content: Content that will be shown as a description of the role.
        :return: Nothing
        """
        reaction_role_embed = Embed().from_dict({
            'title': "Reaction Role",
            'color': 1209873,
            'description': f"{role.mention} rolünü almak için {emoji}'ye tıklayın!"
        })
        reaction_role_embed.set_footer(text=content)
        # Send the embed and assign it to reaction_role_message.
        reaction_role_message = await ctx.send(embed=reaction_role_embed)
        # Add reaction to the message so that members can use it too.
        await reaction_role_message.add_reaction(emoji)
        # Add entry to the database   #MessageID #RoleID
        await fetch_from_server(ctx.guild.id, f"""INSERT INTO ReactionRoles 
                                              VALUES({reaction_role_message.id}, {role.id})""")

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) and "role" in str(error).lower():
            await ctx.send("Belirtilen rol bulunamadı :|")
        if isinstance(error, commands.BadArgument) and "emoji" in str(error).lower():
            await ctx.send("Belirtilen emoji bulunamadı :|")

    @reactionroles.command()
    @is_mod()
    @commands.guild_only()
    async def remove(self, ctx: commands.Context, message_id: int):
        """
        Removes the ReactionRole the message_id is associated with.
        An alternative to the command is to simply delete the message,
        which is checked at 'on_message_delete' in 'guild_listeners.py'.
        :param ctx: Context that was passed during command invocation
        :param message_id: Id of the message the reaction role is given out at.
        :return:
        """
        # If message_id is not a ReactionRole message,
        if (message_id, ) not in await fetch_from_server(ctx.guild.id,
                                                         "SELECT MessageID FROM ReactionRoles"):
            # Send confirmation message, and return False, indicating failure.
            await ctx.send("Mesaj bulunamadı :{")
            return False
        # Fetch the message from the channel the command was invoked from.
        message = await ctx.channel.fetch_message(message_id)
        # Delete the message
        await message.delete()
        # Delete the entry in the database
        await fetch_from_server(ctx.guild.id, f"DELETE FROM ReactionRoles WHERE MessageID = {message_id}")


def setup(client):
    client.add_cog(ReactionRoles(client))
