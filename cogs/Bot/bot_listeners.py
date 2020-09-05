from discord.ext import commands
from discord import Status, Streaming, Forbidden
from os import listdir, mkdir
from codecs import open
import aiosqlite
from scripts.utility import fetch_from_server


class BotListeners(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def create_databases(self, db_name):
        db = await aiosqlite.connect(db_name)
        cs = await db.cursor()
        await cs.execute("""CREATE TABLE Meta(
        Prefix TEXT,
        AdminRoleID INT,
        ModRoleID INT,
        HelperRoleID INT,
        MembercountChannelID INT,
        Volume REAL
        );""")
        # Initilize Meta
        await cs.execute(f"INSERT INTO Meta VALUES('runa ', Null, Null, Null, Null, 1.0)")
        await cs.execute("""CREATE TABLE Members(
        MemberID INT NOT NULL,
        Warnings INT
        );""")
        await cs.execute("""CREATE TABLE Giveaways(
        GuildID INT NOT NULL,
        ChannelID INT NOT NULL,
        MessageID INT NOT NULL,
        EndTime INT,
        Participants TEXT
        );""")
        await cs.execute("""CREATE TABLE ReactionRoles(
        MessageID INT NOT NULL,
        RoleID INT NOT NULL,
        Emoji TEXT NOT NULL
        );""")


        await db.commit()
        await db.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.CheckAnyFailure):
            await ctx.send("Bunu yapmak için yetkiniz yok :|")

        if isinstance(error, Forbidden):
            await ctx.send("Bunu yapmak için yeterli yetkim yok! Yetkilerimi yükseltmeyi deneyin :|")

    @commands.Cog.listener()
    async def on_ready(self):
        server_file_list = listdir('servers')
        for guild in self.client.guilds:
            if str(guild.id) + '.db' not in server_file_list:
                print("Guild {0} is not in server files. Creating...".format(guild.name))
                with open('servers/' + str(guild.id) + '.db', 'w+', encoding="utf-8") as file:
                    file.close()
                await self.create_databases('servers/' + str(guild.id) + '.db')

            membercount_channel = (await fetch_from_server(guild.id, "SELECT MembercountChannelID FROM Meta"))[0][0]

            if membercount_channel:
                membercount_channel = guild.get_channel(membercount_channel)
                await membercount_channel.edit(name="Kullanıcı sayısı: {}".format(len(guild.members)))
        runa_activity = Streaming(platform="Youtube",
                                  name="天球、彗星は夜を跨いで",
                                  url="https://www.youtube.com/watch?v=zLak0dxBKpM")  # Hologram Circus
        await self.client.change_presence(status=Status.online, activity=runa_activity)
        print("We're logged in as: {0}".format(self.client.user))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server_file_list = listdir('servers')
        if str(guild.id) not in server_file_list:
            print("Guild {0} is not in server files. Creating...".format(guild.name))
            if str(guild.id) + '.db' not in server_file_list:
                print("Guild {0} is not in server files. Creating...".format(guild.name))
                with open('servers/' + str(guild.id) + '.db', 'w+', encoding="utf-8") as file:
                    file.close()
                await self.create_databases('servers/' + str(guild.id) + '.db')


def setup(client):
    client.add_cog(BotListeners(client))
