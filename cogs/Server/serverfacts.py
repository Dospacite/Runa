from discord.ext import commands
from discord import Member, Embed
from datetime import date
from scripts.utility import days_to_human_time


class Server(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='serverfacts',
                      help="Sunucu içinde çeşitli bilgileri gösterir.",
                      aliases=['facts', 'guildfacts'])
    @commands.guild_only()
    async def serverfacts(self, ctx, *, guild: str = None):
        """
        ServerFacts is a function that returns interesting information from a server.
        The function loops through the user_dict which contains members and values collected from the server
        For each index in user_dict, it checks the same index in member list and compares those values
        If the members' value is higher (or for index 0, youngest member, lower) replaces the member
        :param ctx: discord.Context Passed by default
        :param guild: Guild that this information will be fetched from.
        :return: None, sends the embed to the ctx channel.
        """
        if not guild:
            guild = ctx.guild
        user_dict = [
            [Member, 99999999],  # youngest(account age) member
            [Member, -1],  # oldest(account age) member
            [Member, 99999999],  # newest member
            [Member, -1],  # oldest member
            [Member, -1],  # oldest premium
            [Member, -1],  # most flags
            [Member, -1],  # longest name
            [Member, -1]  # most roles
        ]
        for member in guild.members:
            member_info = [
                (date.today() - member.created_at.date()).days,  # youngest (age)
                (date.today() - member.created_at.date()).days,  # oldest (age)
                (date.today() - member.joined_at.date()).days,  # newest
                (date.today() - member.joined_at.date()).days,  # oldest (join)
                (date.today() - member.premium_since.date()).days if member.premium_since else 0,  # premium
                len(member.public_flags.all()),  # most flags
                len(member.name),  # longest name
                len(member.roles)  # most roles
            ]
            for fact_index in range(len(user_dict)):
                if (fact_index == 0 or fact_index == 2) and user_dict[fact_index][1] > member_info[fact_index]:
                    user_dict[fact_index][0] = member
                    user_dict[fact_index][1] = member_info[fact_index]
                elif user_dict[fact_index][1] < member_info[fact_index]:
                    user_dict[fact_index][0] = member
                    user_dict[fact_index][1] = member_info[fact_index]
        facts_embed = Embed().from_dict({
            "title": f"{guild.name} Sunucusunun 'En'leri",
            "color": 12150599,
            "fields": [
                {
                    "name": "En Genç Kullanıcı",
                    "value": "{0}\n{1}'dür Discord'da"
                             .format(user_dict[0][0].mention,
                                     "%s Yıl %s Ay %s Gün" % days_to_human_time(user_dict[0][1])),
                    "inline": False
                },
                {
                    "name": "En Yaşlı Kullanıcı",
                    "value": "{0}\n{1}'dür Discord'da"
                             .format(user_dict[1][0].mention,
                                     "%s Yıl %s Ay %s Gün" % days_to_human_time(user_dict[1][1])),
                    "inline": False
                },
                {
                    "name": "En Yeni Üye",
                    "value": "{0}\n{1}'dür {2}'da"
                             .format(user_dict[2][0].mention,
                                     "%s Yıl %s Ay %s Gün" % days_to_human_time(user_dict[2][1]),
                                     guild.name),
                    "inline": False
                },
                {
                    "name": "En Eski Üye",
                    "value": "{0}\n{1}'dür {2}'da"
                             .format(user_dict[3][0].mention,
                                     "%s Yıl %s Ay %s Gün" % days_to_human_time(user_dict[3][1]),
                                     guild.name),
                    "inline": False
                },
                {
                    "name": "En Uzun Süre Premium",
                    "value": "{0}\n{1}'dır Premium Kullanıcısı"
                             .format(user_dict[4][0].mention, user_dict[4][1])
                    if user_dict[4][1] > 0 else "Kimse Premium Kullanmıyor :(",
                    "inline": False
                },
                {
                    "name": "En Çok Bayrak",
                    "value": "{0}\n{1} Tane Bayrağı Var!"
                             .format(user_dict[5][0].mention, user_dict[5][1])
                    if user_dict[5][1] > 0 else "Kimse'nin Bayrağı Yok :(",
                    "inline": False
                },
                {
                    "name": "En Uzun İsim",
                    "value": "{0}\n{1} Karakterli Bir İsmi Var!"
                             .format(user_dict[6][0].mention, user_dict[6][1]),
                    "inline": False
                },
                {
                    "name": "En Çok Rol",
                    "value": "{0}\n{1} Tane Rolü Var!"
                             .format(user_dict[7][0].mention, user_dict[7][1] - 1)
                    if user_dict[7][1] - 1 > 0 else "Kimse'nin Rolü Yok :(",
                    "inline": False
                }
            ]
        })
        facts_embed.set_thumbnail(url=str(guild.icon_url))
        await ctx.send(embed=facts_embed)


def setup(client):
    client.add_cog(Server(client))
