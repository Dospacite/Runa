from discord.ext import commands, tasks
from discord import Embed
import datetime
import time
from random import choice
from scripts.utility import fetch_from_server
from scripts.checks import is_mod


class Giveaways(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_for_done_giveaways.start()

    async def check_for_giveaways(self, guild_id):
        """

        :param guild_id: Id of the guild that will be used to get the database for giveaways
        :return: True if no interruption was made, None if guild does not have any giveaways
        """
        if not await fetch_from_server(guild_id, f"SELECT * FROM Giveaways"):  # If no giveaways are present,
            # Return None for simplicity.
            return None
        finished_giveaways = await fetch_from_server(guild_id,  # Get giveaways that have ended
                                                     f"SELECT * FROM Giveaways WHERE EndTime < {int(time.time())}")
        finished_giveaways = [event for event in finished_giveaways]  # Parse giveaways for better usability
        if finished_giveaways:  # If there are giveaways that have ended,
            # Call end_giveaway for each one.
            for giveaway in finished_giveaways:
                await self.end_giveaway(guild_id,
                                        giveaway[1],
                                        giveaway[2],
                                        giveaway[4].split(',') if giveaway[4] else [])
        return True

    async def end_giveaway(self, guild_id, channel_id, message_id, participants):
        guild = self.client.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        # Randomly pick a winner from the participant list, if noone has joined assign it None
        winner = guild.get_member(int(choice(participants))) if participants else None
        embed = Embed().from_dict({
            'title': "Çekiliş Bitti!",
            'color': 1009273,
            'fields': [
                {
                    'name': "Kazanan: ",
                    'value': winner.mention if winner else "Yok :("
                }
            ]
        })
        await message.edit(embed=embed)
        # Delete giveaway from guild records
        await fetch_from_server(guild_id, f"DELETE FROM Giveaways WHERE MessageID = {message_id}")

    @commands.group(name="giveaways", help="Çekiliş yaratır, düzenler ve siler.", aliases=["giveaway", "çekiliş"])
    @commands.guild_only()
    @is_mod()
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.giveaway.commands])))

    @giveaway.command()
    async def create(self, ctx, time_in_minutes: float, giveaway_topic: str, *, prize: str = None):
        # Get giveaway end time in Epoch time format, by adding 'time_in_minutes' * 60 to the current time
        giveaway_end_time = datetime.datetime.fromtimestamp(int(time_in_minutes * 60 + time.time()))
        # Get giveaway end date for readibility
        giveaway_end_date_str = "{0}/{1}/{2}".format(giveaway_end_time.date().day,
                                                     giveaway_end_time.date().month,
                                                     giveaway_end_time.date().year)
        # Seperate time from date for readibility
        giveaway_end_time_str = "{0}.{1}".format(giveaway_end_time.time().hour,
                                                 giveaway_end_time.time().minute)
        giveaway_embed = Embed().from_dict({
            'title': f"Çekiliş - {giveaway_topic if giveaway_topic else ''}",
            'color': 1209873,
            'description': "Katılmak için 🎊'ye tıklayın :|",
            'fields': [
                {
                    'name': "Ödül:",
                    'value': prize if prize else "Yok :("
                }
            ]
        })
        giveaway_embed.set_footer(text=f"Bitiş Zamanı: {giveaway_end_date_str} {giveaway_end_time_str}")
        giveaway_message = await ctx.send(embed=giveaway_embed)
        await giveaway_message.add_reaction("🎊")
        # Create a giveaway entry in the database
        await fetch_from_server(ctx.guild.id,
                                f"""INSERT INTO Giveaways 
                                    VALUES({ctx.guild.id}, 
                                            {giveaway_message.channel.id}, 
                                            {giveaway_message.id},
                                            {int(time_in_minutes * 60 + time.time())},
                                            NULL);""")

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send(f"Kullanım: {ctx.prefix}giveaway create [emoji] [dakika] [başlık] [ödül]")

    @tasks.loop(minutes=1)
    async def check_for_done_giveaways(self):
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            # Loop through all the guilds to check for giveaways
            await self.check_for_giveaways(guild.id)


def setup(client):
    client.add_cog(Giveaways(client))
