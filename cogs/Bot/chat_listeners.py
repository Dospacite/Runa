from discord.ext import commands


class ChatListeners(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(ChatListeners(client))
