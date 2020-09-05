from discord.ext import commands
from json import load, dump
from scripts.checks import is_helper


class Tagging(commands.Cog):

    def __init__(self, client):
        self.client = client

    def get_tag_dict(self):
        with open('json/tags.json') as file:
            tags = dict(load(file))
        return tags

    def get_tag(self, tag):
        tags = self.get_tag_dict()
        return tags.get(tag)

    def set_tag(self, tag, content):
        tags = self.get_tag_dict()
        tags[tag] = content
        with open('json/tags.json', 'w') as file:
            dump(tags, file)

    def del_tag(self, tag):
        tags = self.get_tag_dict()
        if not tags.get(tag):
            return False
        tags.pop(tag)
        with open('json/tags.json', 'w') as file:
            dump(tags, file)
        return True

    @commands.group(name="tags", help="Tagları gösterir, değiştirir veya siler.", aliases=["etiket", "tag"])
    async def tags(self, ctx):
        if ctx.invoked_subcommand is None:
            tag_list = list(self.get_tag_dict().keys())
            await ctx.send("Mevcut Taglar: ```{0}```".format(", ".join(tag_list) if tag_list else "Hiç tag yok :("))

    @tags.command(name="show", help="Tag gösterir.", aliases=['göster'])
    async def show(self, ctx, tag):
        tag_content = self.get_tag(tag)
        if not tag_content:
            await ctx.send(f"Tag {tag} bulunamadı :|")
        await ctx.send(tag_content)

    @tags.command(name="add", help="Tag ekler.", aliases=['ekle'])
    async def add(self, ctx, tag, *, content=None):
        if self.get_tag(tag):
            await ctx.send("Bu tag zaten mevcut :|")
            return False
        if content:
            self.set_tag(tag, content)
        else:
            self.set_tag(tag, (await ctx.channel.history(limit=1, before=ctx.message).flatten())[0].content)
        await ctx.send(f"Tag {tag} başarıyla eklendi :|")

    @tags.command(name="remove", help="Tag siler.", aliases=['sil', 'del'])
    async def remove(self, ctx, tag):
        deletion = self.del_tag(tag)
        if not deletion:
            await ctx.send("Tag bulunamadı :|")
            return False
        await ctx.send(f"Tag {tag} başarıyla silindi :|")

    @tags.command(name="set", help="Tag ayarlar.", aliases=['ayarla'])
    @is_helper()
    async def set(self, ctx, tag, *, content):
        self.set_tag(tag, content)
        await ctx.send(f"Tag {tag} başarıyla ayarlandı :|")


def setup(client):
    client.add_cog(Tagging(client))
