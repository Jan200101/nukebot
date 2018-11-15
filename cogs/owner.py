from sys import exit as sysexit
from discord.ext import commands
from discord import Member


class owner:
    """
    """

    def __init__(self, bot):
        self.bot = bot
        self.guilds = []
        print(
            "[Owner] all command messages are printed in the console, watch out for them")

    @commands.command(name="exit")
    async def _exit(self, ctx):
        """
        Shutdown the bot
        """
        await self.bot.logout()
        sysexit(0)

    @commands.group()
    async def users(self, ctx):
        """
        Manage allowed users
        """
        if ctx.invoked_subcommand is None:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    @users.command(name="add")
    async def adduser(self, ctx, user: Member):
        """
        allowed  users
        """
        if user.id in self.bot.allowedusers.id:
            print("[Owner] User already allowed")
            return
        self.bot.allowedusers.id.append(user.id)
        print("[Owner] User allowed")
        self.bot.allowedusers.save()

    @users.command(name="remove")
    async def deluser(self, ctx, user: Member):
        """
        disallow users
        """
        try:
            self.bot.allowedusers.id.remove(str(user.id))
            print("[Owner] User no longer allowed")
            self.bot.allowedusers.save()
        except ValueError:
            print("[Owner] User already not allowed")


def setup(bot):
    b = owner(bot)
    bot.add_cog(b)
