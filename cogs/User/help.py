from discord.ext import commands
from discord import Embed


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help",
                      help="Runa'nın tüm komutlarını ve hakkındaki bilgileri gösterir.",
                      aliases=["yardım"])
    async def help(self, ctx, command=None):
        help_embed = None
        if command:
            searched_command = self.client.get_command(command)
            if searched_command:
                help_embed = Embed(title=f"{searched_command.name.title()} Komutu", color=12150599)
                help_embed.add_field(name=searched_command.name.title(), value=searched_command.help)
                if type(searched_command) == commands.Group:
                    for command in searched_command.commands:
                        help_embed.add_field(name=f"{searched_command.name} {command.name}",
                                             value=command.help, inline=False)
        else:
            help_embed = Embed(title=f"Runa'nın komutları ({len(self.client.commands)} Komut!)", color=12150599)
            for command in self.client.commands:
                help_embed.add_field(name=command.name.title(), value=command.help)

        if not help_embed:
            help_embed = Embed().from_dict({'title': "Belirtilen komut bulunamadı :|", 'color': 12150599})
        await ctx.send(embed=help_embed)


def setup(client):
    client.add_cog(Help(client))
