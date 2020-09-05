from discord.ext import commands
from discord import Status, Member
from scripts.language import TR


class Mention(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='mention', help="Belirtilen kullanıcıyı pingler.", aliases=['bahset'])
    @commands.guild_only()
    async def mention(self, ctx, *, member: Member):
        if member.status != Status.do_not_disturb:
            await ctx.send("{0}! {1} seni pingledi!".format(member.mention, ctx.author.mention))
        else:
            await ctx.send("Kullanıcı rahatsız etmeyin modunda :|")

    @mention.error
    async def mention_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))


def setup(client):
    client.add_cog(Mention(client))
