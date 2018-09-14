from sys import exit as sysexit
from discord.ext import commands
from discord import Member


class owner:
    """
    """

    def __init__(self, bot):
        self.bot = bot
        self.guilds = []
        try:
            self.bot.allowedusers = open(
                "config/allowedusers.txt").read().split("\n")
        except:
            with open("config/allowedusers.txt", "w") as config:
                config.write("")
            self.bot.allowedusers = []
        print(
            "[Owner] all command messages are printed in the console, watch out for them")

    @commands.command(name="exit")
    async def _exit(self, ctx):
        self.bot.logout()
        sysexit()

    @commands.group()
    async def users(self, ctx):
        return

    @users.command(name="add")
    async def adduser(self, ctx, user: Member):
        """Add allowed users"""
        if str(user.id) in self.bot.allowedusers:
            print("[Owner] User already allowed")
            return
        self.bot.allowedusers.append(str(user.id))
        print("[Owner] User allowed")
        with open("config/allowedusers.txt", "w") as config:
            config.write("\n".join(self.bot.allowedusers))

    @users.command(name="remove")
    async def deluser(self, ctx, user: Member):
        try:
            self.bot.allowedusers.remove(str(user.id))
            print("[Owner] User no longer allowed")
        except ValueError:
            print("[Owner] User already not allowed")

    @users.command()
    async def reload(self, ctx):
        """Reload allowed users"""
        try:
            self.bot.allowedusers = open(
                "config/allowedusers.txt").read().split("\n")
            print("[Owner] User config reloaded")
        except:
            with open("config/allowedusers.txt", "w") as config:
                config.write("")
            self.bot.allowedusers = []


def setup(bot):
    b = owner(bot)
    bot.add_cog(b)
    bot.loop.create_task(b.auditspam())
