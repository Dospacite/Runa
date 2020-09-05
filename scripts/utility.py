from .JSON import JSON
from discord.utils import find
import aiosqlite


def days_to_human_time(days):
    years = days // 365
    days %= 365
    months = days // 30
    days %= 30
    return years, months, days


async def fetch_from_server(guild_id, query):
    db = await aiosqlite.connect('servers/' + str(guild_id) + '.db')
    cs = await db.cursor()
    await cs.execute(query)
    value = await cs.fetchall()
    await db.commit()
    await db.close()
    return value


async def get_member_from_name(ctx, name):
    return find(lambda member: member.name.lower() == name.lower(), ctx.guild.members)
