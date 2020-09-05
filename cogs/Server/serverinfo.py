from discord.ext import commands
from discord.utils import get
from discord import Embed
from scripts.utility import days_to_human_time
from scripts.language import TR
from datetime import date


class Server(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='server',
                      help="Sunucu bilgilerini gösterir.",
                      aliases=['guild', 'serverinfo', 'guildinfo', 'sunucu'])
    @commands.guild_only()
    async def guildinfo(self, ctx, *, guild: str = None):
        if not guild:
            guild = ctx.guild
        else:
            guild = get(self.client.guilds, name=guild)
        guild_embed = Embed().from_dict({
            "title": str(guild.name),
            "description": f"Information about the server: {guild.name}",
            "author": {
                "name": guild.name,
                "icon_url": str(guild.icon_url)
            },
            "color": 53380,
            "fields": [
                {
                    "name": "Server Region:",
                    "value": str(guild.region).title(),
                    "inline": False
                },
                {
                    "name": "Server ID:",
                    "value": str(guild.id),
                    "inline": False
                },
                {
                    "name": "Owner Name:",
                    "value": str(guild.owner.mention),
                    "inline": False
                },
                {
                    "name": "Member Count:",
                    "value": str(guild.member_count),
                    "inline": False
                },
                {
                    "name": "Text Channel Count:",
                    "value": str(len(guild.text_channels)),
                    "inline": False
                },
                {
                    "name": "Voice Channel Count:",
                    "value": str(len(guild.voice_channels)),
                    "inline": False
                },
                {
                    "name": "Created At:",
                    "value": "{0}.{1}.{2} {3}:{4}"
                             .format(guild.created_at.day, guild.created_at.month, guild.created_at.year,
                                     guild.created_at.hour, guild.created_at.minute),
                    "inline": False
                },
                {
                    "name": "Guild Age:",
                    "value": "%s Years, %s Months and %s Days"
                             % days_to_human_time((date.today() - guild.created_at.date()).days),
                    "inline": False
                },
                {
                    "name": "AFK Channel:",
                    "value": str(guild.afk_channel.mention),
                    "inline": False
                }
            ]
        })
        guild_embed.set_thumbnail(url=str(guild.icon_url))
        await ctx.send(embed=guild_embed)

    @guildinfo.error
    async def guildinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(TR().dict.get('SERVER_NOT_FOUND'))


def setup(client):
    client.add_cog(Server(client))
