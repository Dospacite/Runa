from discord.ext import commands
from os import listdir, path
from scripts.JSON import JSON
from scripts.utility import fetch_from_server


async def get_prefix(client_, message):
    if message.guild:  # If message was sent from a guild
        # Connect to guild database and create a cursor
        prefix = await fetch_from_server(message.guild.id,
                                         "SELECT Prefix FROM Meta")
        if prefix:
            return commands.when_mentioned_or(prefix[0][0])(client_, message)
    return commands.when_mentioned_or("runa ")(client_, message)


config = JSON('./json/config.json').dict
client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')

for foldername in listdir('cogs'):
    if path.isdir('cogs/' + foldername):
        for filename in listdir('cogs/' + foldername):
            if filename.endswith('.py'):
                client.load_extension(f"cogs.{foldername}.{filename[:-3]}")


client.run(config.get('token'))
