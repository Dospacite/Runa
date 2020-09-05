from discord.ext import commands
from discord import Embed, File
from PIL.ImageColor import getrgb
from PIL.Image import new, effect_mandelbrot
from PIL import ImageDraw
from io import BytesIO
from scripts.language import TR
from random import randint, random


class Colors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_color_file(color_str):
        color_ = getrgb(color_str)
        img = new(mode="RGB", size=(512, 512), color=color_)
        with BytesIO() as image_bin:
            img.save(image_bin, "PNG")
            image_bin.seek(0)
            color_file = File(image_bin, filename="color.png")

        return color_file

    @staticmethod
    def get_color_embed(color_str):
        color_embed = Embed().from_dict(
            {
                "title": "Renk Bilgileri",
                "color": int('%02x%02x%02x' % getrgb(color_str), 16),
                "fields": [
                    {
                        "name": "RGB",
                        "value": str(getrgb(color_str)),
                        "inline": True
                    },
                    {
                        "name": "HEX",
                        "value": '#%02x%02x%02x' % getrgb(color_str),
                        "inline": True
                    },
                    {
                        "name": "Decimal",
                        "value": int('%02x%02x%02x' % getrgb(color_str), 16),
                        "inline": True
                    }
                ]
            })
        return color_embed

    @commands.command(name='color',
                      help="Belirtilen rengin fotoğrafını yollar.")
    async def color(self, ctx, *colors):
        colors = list(colors)
        horizontal = True
        for n, color in enumerate(colors):
            if color.lower() == 'random':
                colors[n] = "rgb({0}, {1}, {2})".format(randint(0, 255), randint(0, 255), randint(0, 255))
            if color.lower() == 'vertical':
                horizontal = False
                colors.pop(n)
        color_ = getrgb(colors[-1])
        img = new(mode="RGB", size=(512, 512), color=color_)
        img_draw = ImageDraw.Draw(img)
        if not horizontal:
            for color_index in range(len(colors)):
                img_draw.rectangle(xy=((color_index*(512//len(colors)), 0), ((color_index+1)*(512//len(colors)), 512)),
                                   fill=colors[color_index])
        else:
            for color_index in range(len(colors)):
                img_draw.rectangle(xy=(0, (color_index*(512//len(colors))), (512, (color_index+1)*(512//len(colors)))),
                                   fill=colors[color_index])
        with BytesIO() as image_bin:
            img.save(image_bin, "PNG")
            image_bin.seek(0)
            color_file = File(image_bin, filename="color.png")
            if len(colors) == 1:
                color_embed = Colors.get_color_embed(colors[0])
                color_embed.set_image(url="attachment://color.png")
                await ctx.send(file=color_file, embed=color_embed)
            else:
                await ctx.send(file=color_file)

    @color.error
    async def color_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(TR().dict.get('COLOR_NOT_FOUND'))


def setup(client):
    client.add_cog(Colors(client))
