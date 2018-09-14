from json import dump, load
from asyncio import sleep
from discord import TextChannel
from discord.ext import commands
from requests import post, delete


class webhook:
    """
    a botless way of spamming a channel
    manually handles webhooks
    """

    def __init__(self, bot):
        self.bot = bot
        self.payload = {
            "username": "Webhook",
            "content": "SPAM"
        }
        self.spamlist = []
        try:
            self.webhooks = load(open("config/webhooks.json"))
        except:
            self.webhooks = {}

    @commands.command()
    async def create(self, ctx, channel: TextChannel=None):
        try:
            await ctx.message.delete()
        except:
            pass  # lets just ignore it

        if not channel:
            channel = ctx.message.channel

        webhook = await channel.create_webhook(name="Webhook")

        try:
            self.webhooks[channel.id].append(webhook.url)
        except:
            self.webhooks[channel.id] = [webhook.url]
        with open("config/webhooks.json", "w") as config:
            dump(self.webhooks, config, indent=4,
                 sort_keys=True, separators=(',', ':'))

    @commands.command()
    async def removeall(self, ctx, channel: TextChannel=None):
        try:
            await ctx.message.delete()
        except:
            pass  # lets just ignore it

        if not channel:
            channel = ctx.message.channel

        while self.webhooks[channel.id]:
            try:
                url = self.webhooks[channel.id].pop(0)
                delete(url)
            except:
                pass

        with open("config/webhooks.json", "w") as config:
            dump(self.webhooks, config)

    @commands.command()
    async def startspam(self, ctx, channel: TextChannel=None):
        try:
            await ctx.message.delete()
        except:
            pass  # lets just ignore it

        if not channel:
            channel = ctx.message.channel

        self.spamlist.append(channel.id)
        print("[Spam] Added {} to spamlist".format(channel.name))

    @commands.command()
    async def stopspam(self, ctx, channel: TextChannel=None):
        try:
            await ctx.message.delete()
        except:
            pass  # lets just ignore itß

        if not channel:
            channel = ctx.message.channel

        self.spamlist.remove(channel.id)
        print("[Spam] Removed {} to spamlist".format(channel.name))

    async def spamtask(self):
        await self.bot.wait_until_ready()
        # loop while this cog is loaded
        while self == self.bot.get_cog('webhook'):
            for id in self.spamlist:
                for url in self.webhooks[id]:

                    response = post(url, json=self.payload)

                    if response.status_code != 200:
                        print("Invalid Response from:\n{}\nResponse:\n{}\n".format(
                            url, response.text))

                    try:
                        # ratelimiting happens more than you'd think
                        print("Being Ratelimit, {}s".format(
                            response.json()["retry_after"]))
                        await sleep(response.json()["retry_after"])
                    except:
                        print("no ratelimit")
            await sleep(1)


def setup(bot):
    b = webhook(bot)
    bot.add_cog(b)
    bot.loop.create_task(b.spamtask())
