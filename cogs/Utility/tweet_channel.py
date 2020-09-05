from discord.ext import commands, tasks
from discord import TextChannel
from scripts.JSON import JSON
from aiohttp_requests import requests


class Tweets(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tweet_json = JSON('json/tweets.json')

    @staticmethod
    async def get_twitter_user_id_by_username(username):
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {"authorization": f"Bearer {JSON('json/auth.json').dict.get('twitter').get('bearer-token')}"}
        request = await requests.get(url, headers=headers)
        tweet_id = dict(await request.json())
        return tweet_id

    @staticmethod
    async def get_tweets_by_username(name):
        url = "https://api.twitter.com/2/tweets/search/recent?query=from:{0}".format(name)
        headers = {"authorization": f"Bearer {JSON('json/auth.json').dict.get('twitter').get('bearer-token')}"}
        request = await requests.get(url, headers=headers)
        tweets_dict = dict(await request.json())
        return tweets_dict

    @staticmethod
    def get_last_tweet(name):
        tweets = Tweets.get_tweets_by_username(name)
        return tweets[0] if tweets else None

    @commands.group(name="tweets",
                    help="Bir kanala twitter gönderilerini işler, kaldırır veya ayarlar.",
                    aliases=["twitter", "tweet"])
    async def tweets(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Mevcut altkomutlar: {0}"
                           .format(", ".join([command.name for command in self.tweets.commands])))

    @tweets.command(name="bind",
                    help="Bu kanala bir Twitter hesabındaki gönderileri işler.",
                    aliases=["işle"])
    async def bind(self, ctx, twitter_name: str, channel: TextChannel = None):
        if not channel:  # If channel is not specified,
            # Then the target channel is the one the message was sent in.
            channel = ctx.channel
        # Get user id of twitter account for easy usage.
        user_info = Tweets.get_twitter_user_id_by_username(twitter_name)
        # If twitter user was referenced before, and the guild is already subscribed to it in the same channel,
        if self.tweet_json.dict.get(user_info.get('username')) \
           and {"guild": ctx.guild.id, "channel": channel.id} in self.tweet_json.dict.get(user_info.get('username')):
            # Raise KeyError which is handled below.
            raise KeyError

    @bind.error
    async def bind_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Bu kanal zaten bu Twitter hesabına bağlı :|")

    @staticmethod
    async def get_tweet_embed(tweet_id, author):
        query = "?tweet.fields=attachments,author_id,created_at,entities,id,source,text,withheld"
        url = f"https://api.twitter.com/2/tweets/{tweet_id}" + query
        headers = {"authorization": f"Bearer {JSON('json/auth.json').dict.get('twitter').get('bearer-token')}"}
        request = await requests.get(url, headers=headers)

    @tasks.loop(minutes=5)
    async def check_for_tweets(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Tweets(client))
