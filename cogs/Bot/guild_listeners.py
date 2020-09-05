from discord.ext import commands
from scripts.utility import fetch_from_server


class GuildListeners(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        membercount_channel = member.guild.get_channel(
            (await fetch_from_server(member.guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0]
        )
        if membercount_channel:
            await membercount_channel.edit(name="Kullanıcı sayısı: {}".format(len(member.guild.members)))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        membercount_channel = member.guild.get_channel(
            (await fetch_from_server(member.guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0]
        )
        if membercount_channel:
            await membercount_channel.edit(name="Kullanıcı sayısı: {}".format(len(member.guild.members)))

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        guild_giveaways = await fetch_from_server(payload.guild_id, "SELECT MessageID FROM Giveaways")
        guild_reactionroles = await fetch_from_server(payload.guild_id, "SELECT MessageID FROM ReactionRoles")
        if guild_giveaways and (payload.message_id, ) in guild_giveaways:
            print('reached')
            await fetch_from_server(payload.guild_id,
                                    f"DELETE FROM Giveaways WHERE MessageID = {payload.message_id}")
        if guild_reactionroles and (payload.message_id, ) in guild_reactionroles:
            await fetch_from_server(payload.guild_id,
                                    f"DELETE FROM ReactionRoles WHERE MessageID = {payload.message_id}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (not member.bot) and after and after.afk:  # If the member is not a Bot, did not leave, and is AFK,
            if "UN-AFK" in [role.name for role in member.roles]:  # Check for UN-AFK role,
                if before:  # Check if they did NOT willingly joined AFK
                    await member.edit(voice_channel=before.channel)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
        message = await self.client.get_guild(payload.guild_id)\
                            .get_channel(payload.channel_id)\
                            .fetch_message(payload.message_id)
        message_id_str = str(payload.message_id)

        if not user.bot:
            # Reaction Roles
            server_events_reaction_roles = \
                await fetch_from_server(payload.guild_id, "SELECT MessageID FROM ReactionRoles")
            # If server has reaction roles set and reacted message is in that dict,
            if server_events_reaction_roles and (message.id, ) in server_events_reaction_roles:
                # Than add the role to the reacted member
                await user.add_roles(message.guild.get_role(
                    (await fetch_from_server(payload.guild_id,
                                             f"""SELECT RoleID FROM ReactionRoles 
                                             WHERE MessageID = {message.id}"""))[0][0]))
            # Giveaways
            server_events_giveaways = await fetch_from_server(payload.guild_id, "SELECT MessageID FROM Giveaways")
            if server_events_giveaways and (message.id, ) in server_events_giveaways:
                participants = (await fetch_from_server(message.guild.id,
                                                        f"""SELECT Participants FROM Giveaways 
                                                            WHERE MessageID = {message.id}"""))[0][0]

                # These 4 lines of code basically parses the string and appends the list
                part_list = participants.split(",") if participants else []
                part_list.append(str(user.id))
                part_list = part_list if part_list else None
                participants = ','.join(part_list) if part_list else 'NULL'

                print(participants)

                await fetch_from_server(message.guild.id,
                                        f"UPDATE Giveaways SET Participants = '{participants}'")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        user = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
        message = await self.client.get_guild(payload.guild_id) \
            .get_channel(payload.channel_id) \
            .fetch_message(payload.message_id)

        if not user.bot:
            # Reaction Roles
            server_events_reaction_roles = \
                await fetch_from_server(payload.guild_id, "SELECT MessageID FROM ReactionRoles")
            # If server has reaction roles set and reacted message is in that dict,
            if server_events_reaction_roles and (message.id, ) in server_events_reaction_roles:
                # Than remove the role from the reacted member
                await user.remove_roles(message.guild.get_role(
                    (await fetch_from_server(payload.guild_id,
                                             f"""SELECT RoleID FROM ReactionRoles 
                                                 WHERE MessageID = {message.id}"""))[0][0]))
            # Giveaways
            server_events_giveaways = await fetch_from_server(payload.guild_id, "SELECT MessageID FROM Giveaways")
            if server_events_giveaways and (message.id, ) in server_events_giveaways:
                participants = (await fetch_from_server(message.guild.id,
                                                        f"""SELECT Participants FROM Giveaways 
                                                            WHERE MessageID = {message.id}"""))[0][0]

                # These 4 lines of code basically parses the string and removes from the list
                part_list = participants.split(",") if participants else []
                part_list.remove(str(user.id))
                part_list = part_list if part_list else None
                participants = ','.join(part_list) if part_list else 'NULL'

                print(participants)

                await fetch_from_server(message.guild.id,
                                        f"UPDATE Giveaways SET Participants = {participants}")


def setup(client):
    client.add_cog(GuildListeners(client))
