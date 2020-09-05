from discord.ext import commands
from discord import User, Member, Embed
from typing import Union
from datetime import date
from scripts.utility import days_to_human_time
from scripts.language import TR
from PIL import Image


class UserInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='user',
                      help="Kullanıcının bilgilerini gösterir.",
                      aliases=['kullanıcı', 'userinfo.py'])
    async def userinfo(self, ctx, *, member: Union[User, Member] = None):
        if not member:
            member = ctx.author
        user_embed = Embed().from_dict(dict({
            "title": str(member.name),
            "description": "Information about {0}".format(member.name),
            "author": {
                "name": str(member.name),
                "icon_url": str(member.avatar_url)
            },
            "color": 12150599,
            "fields": [
                {
                    "name": "User ID:",
                    "value": str(member.id),
                    "inline": False
                },
                {
                    "name": "Joined Discord At:",
                    "value": "{0}.{1}.{2} {3}:{4}"
                        .format(member.created_at.day, member.created_at.month, member.created_at.year,
                                member.created_at.hour, member.created_at.minute),
                    "inline": False
                },
                {
                    "name": "Account Age:",
                    "value": "%s Years,  %s Months and %s Days"
                             % days_to_human_time((date.today() - member.created_at.date()).days),
                    "inline": False
                },
                {
                    "name": "Mention:",
                    "value": str(member.mention),
                    "inline": False
                },
                {
                    "name": "Display Name:",
                    "value": str(member.display_name),
                    "inline": False
                },
                {
                    "name": "Avatar Url:",
                    "value": str(member.avatar_url),
                    "inline": False
                }
            ]
        }))
        user_embed.set_thumbnail(url=str(member.avatar_url))
        await ctx.send(embed=user_embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            await ctx.send(TR().dict.get('USER_NOT_FOUND'))


def setup(client):
    client.add_cog(UserInfo(client))
