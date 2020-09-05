from discord.ext import commands
from discord import User, File, Embed
from typing import Optional
from io import BytesIO


class Avatar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='avatar', help="Kullanıcının avatarını gösterir.")
    async def avatar(self, ctx, user: Optional[User]):
        if not user:
            user = ctx.author
        with BytesIO() as file:
            await user.avatar_url.save(file)
            avatar_embed = Embed(title=f"{user.display_name}'s Avatar", color=182373)
            image = File(file, filename='avatar.webp')
            avatar_embed.set_image(url="attachment://avatar.webp")
            await ctx.send(file=image, embed=avatar_embed)


def setup(client):
    client.add_cog(Avatar(client))
