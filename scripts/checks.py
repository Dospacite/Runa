from discord.ext import commands
from .utility import fetch_from_server


def is_bot_owner():
    async def predicate(ctx):
        return ctx.author.id == 326750191187394570

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id \
                or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                      "SELECT AdminRoleID FROM Meta"))[0][0]) in ctx.author.roles
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id \
            or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                                           "SELECT AdminRoleID FROM Meta"))[0][0]) in ctx.author.roles \
            or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                                           "SELECT ModRoleID FROM Meta"))[0][0]) in ctx.author.roles

    return commands.check(predicate)


def is_helper():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id \
            or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                                           "SELECT AdminRoleID FROM Meta"))[0][0]) in ctx.author.roles \
            or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                                           "SELECT ModRoleID FROM Meta"))[0][0]) in ctx.author.roles \
            or ctx.guild.get_role((await fetch_from_server(ctx.guild.id,
                                                           "SELECT HelperRoleID FROM Meta"))[0][0]) in ctx.author.roles

    return commands.check(predicate)


def can_manage_messages():
    async def predicate(ctx):
        return ctx.author.permissions_in(ctx.channel).manage_messages

    return commands.check(predicate)
