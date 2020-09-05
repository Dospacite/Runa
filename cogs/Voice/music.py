from youtube_dl import YoutubeDL
from asyncio import get_event_loop
from scripts.utility import fetch_from_server
from scripts.checks import is_helper
from discord.ext import commands
from json import loads
from discord import FFmpegPCMAudio, PCMVolumeTransformer, Embed
from youtubesearchpython import SearchVideos

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn -nostdin -loglevel quiet',
    'before_options': "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = YoutubeDL(YTDL_OPTIONS)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {}

    async def get_queue(self, guild_id):
        """
        Returns the music queue of the guild
        :param guild_id: Id of the guild whose music queue will be returned
        :return: Music queue belonging to the guild, None if it doesn't exist
        """
        return self.queues.get(guild_id)

    async def start_queue(self, guild_id):
        """
        Clears the specified guilds music queue or can be used to start a new queue
        :param guild_id: Id of the guild whose queue will be cleared
        :return: Empty list
        """
        self.queues[guild_id] = []
        return []

    async def remove_queue(self, guild_id):
        """
        Removes a guilds queue from the queue dictionary
        :param guild_id: Id of the guild whose queue will be deleted
        :return: Rest of the queues
        """
        del self.queues[guild_id]
        return self.queues

    async def add_to_queue(self, guild_id, url):
        """
        Adds a music url to a guilds music queue
        :param guild_id: Id of the guild whose queue will be appended
        :param url: Music url that will be added to the queue
        :return: New queue with the added url
        """
        self.queues[guild_id].append(url)
        return self.queues[guild_id]

    async def get_source_from_string(self, string: str, volume):
        if "https://www.youtube.com/watch?v=" in string or "https://youtu.be/" in string:
            url = string
        else:
            url = await self.get_video_from_query(string)
        data = await self.get_data_from_url(url)
        embed = await self.get_video_embed(data)
        source = await self.get_audio_source_from_data(data, volume)
        return url, source, embed

    @commands.command(name="play", help="Verilen müziği oynatır.", aliases=["oynat", "oyna"])
    async def play_(self, ctx: commands.Context, query: str):
        volume = (await fetch_from_server(ctx.guild.id, "SELECT Volume FROM Meta"))[0][0]
        url, source, embed = await self.get_source_from_string(query, volume)
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect()
            await self.start_queue(ctx.guild.id)
        if ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused():
            await self.add_to_queue(ctx.guild.id, url)
        else:
            ctx.guild.voice_client.play(source, after=self.after_play)
        if await self.get_queue(ctx.guild.id):
            await self.play_(ctx, (await self.get_queue(ctx.guild.id))[0])

    def after_play(self, error):
        if error:
            print(error)

    async def stop_single(self, ctx):
        if not ctx.guild.voice_client:
            raise Exception("NoVoiceState")
        if ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused():
            await ctx.send("Oynayan parça durduruluyor.")
            ctx.guild.voice_client.stop()
        if await self.get_queue(ctx.guild.id):
            await self.play_(ctx, (await self.get_queue(ctx.guild.id))[0])

    @commands.command(name="stop", help="Müziği bitirir.", aliases=["skip", "bitir", "geç"])
    async def stop_self(self, ctx):
        await self.stop_single(ctx)

    @commands.group(name="audio",
                    help="Sesler ve müzik ile ilgili komutları barındırır.",
                    aliases=["music", "müzik"])
    async def audio(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.audio.commands])))

    @audio.command(name="play", help="Bir linkten veya aramadan müzik oynatır.", aliases=["oynat", "oyna"])
    async def play(self, ctx, *, string: str):
        await self.play_(ctx, string)

    @audio.command(name="stop", help="Oynayan sesi durdurur.", aliases=["bitir", "bit"])
    async def stop(self, ctx):
        await self.stop_single(ctx)

    @audio.command(name="pause", help="Oynayan sesi duraklatır.", aliases=["durdur", "dur"])
    async def pause(self, ctx):
        if not ctx.guild.voice_client:
            raise Exception("NoVoiceState")
        if ctx.guild.voice_client.is_playing() and not ctx.guild.voice_client.is_paused():
            ctx.guild.voice_client.pause()

    @audio.command(name="resume", help="Duraklatılmış sesi oynatmaya devam eder.", aliases=["devam", "devamke"])
    async def resume(self, ctx):
        if not ctx.guild.voice_client:
            raise Exception("NoVoiceState")
        if ctx.guild.voice_client.is_playing() and ctx.guild.voice_client.is_paused():
            ctx.guild.voice_client.resume()

    @audio.command(name="volume", help="Müziğin çalacağı sesin yüksekliğini ayarlar.", aliases=["sesdüzeyi"])
    @is_helper()
    async def volume(self, ctx, volume: float = None):
        if not volume:
            volume = (await fetch_from_server(ctx.guild.id, "SELECT Volume FROM Meta"))[0][0]
            await ctx.send(f"Sunucu ses düzeyi: `{volume}`")
            return True
        await fetch_from_server(ctx.guild.id, f"UPDATE Meta SET Volume = {volume}")
        await ctx.send(f"Ses düzeyi `{volume}`'a ayarlandı :|")

    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Doğru bir ses seviyesi belirtmediniz :|")

    async def get_video_embed(self, video):
        embed = Embed().from_dict({
            'title': f"[{video.get('duration')//60}:{video.get('duration')%60}] - {video.get('title')}",
            'color': 14714208
        })
        embed.set_image(url=video.get('thumbnails')[-1]['url'])
        embed.set_footer(text=f"Yükleyen: {video.get('uploader')}\n"
                              f"İzlenme: {video.get('view_count')}")
        embed.set_author(icon_url=self.client.user.avatar_url, name="Şimdi oynatılıyor...")
        return embed

    async def get_data_from_url(self, url, stream=True):
        loop = get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if not data:
            raise Exception(f"NoVideoFound: Video with the url {url} not found.")
        return data

    @staticmethod
    async def get_video_from_query(query):
        results = loads(SearchVideos(query, max_results=1, mode='json').result())
        if not results:
            raise Exception(f"NoVideoFound: Video with the query {query} not found.")
        results = results['search_result'][0]
        return results['link']

    @staticmethod
    async def get_audio_source_from_data(data, volume: float):
        return PCMVolumeTransformer(FFmpegPCMAudio(data['formats'][0]['url'], **ffmpeg_options), volume)


def setup(client):
    client.add_cog(Music(client))

