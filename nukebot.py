from traceback import format_exception
from os import mkdir, chdir, path
from sys import exit as sysexit
from configparser import ConfigParser
from json import load, dump
from discord.ext import commands

__VERSION__ = (0, 2, 1)

print("Starting Nukebot Version {0[0]}.{0[1]}.{0[2]}\n".format(__VERSION__))

directory = path.dirname(path.realpath(__file__))
chdir(directory)

try:
    mkdir("config")
except:
    pass

# TODO
# faze out ini and add a setup process
config = ConfigParser()
config.read("config.ini")

try:
    bot_prefix = [x.strip() for x in config['Main']['prefix'].split(",")]
except:
    bot_prefix = ["."]

# TODO
# disable DMs
bot = commands.Bot(command_prefix=bot_prefix)


@bot.check_once
def whitelist(ctx):
    if ctx.message.author == bot.owner:
        return True

    if str(ctx.message.author.id) in bot.allowedusers or ctx.message.author.name in bot.allowedusers:
        return True

    return False


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument, commands.DisabledCommand, commands.CommandNotFound, commands.NoPrivateMessage)):
        return
    elif isinstance(error, commands.CommandInvokeError):

        exception_log = "Exception in command '{}'\n" "".format(
            ctx.command.qualified_name)
        exception_log += "".join(
            format_exception(type(error), error, error.__traceback__)
        )
        print(exception_log)


@bot.event
async def on_ready():

    try:
        addons = load(open("config/addons.json"))
    except:
        addons = [
            'owner',
            'nuker',
            'webhook',
        ]
        with open("config/addons.json", "w") as config:
            dump(addons, config, indent=4, sort_keys=True, separators=(',', ':'))

    application = await bot.application_info()
    bot.owner = application.owner

    try:
        bot.allowedusers = open("config/allowedusers.txt").read().split("\n")
    except:
        with open("config/allowedusers.txt", "w") as config:
            config.write("")
        bot.allowedusers = []

    for addon in addons:
        try:
            bot.load_extension("addons." + addon)
            print("{} addon loaded.".format(addon))
        except Exception as e:
            print("Failed to load {} :\n{} : {}".format(
                addon, type(e).__name__, e))

    if bot.guilds:
        print("\nClient logged in as {}, in the following guild(s):".format(
            bot.user.name))
        for guild in bot.guilds:
            print(guild.name)
    else:
        print("\nClient logged in as {}, in no guilds".format(bot.user.name))

bot.login(config['Main']['token'])


if __name__ == "__main__":
    try:
        bot.connect()
    except KeyboardInterrupt:
        bot.logout()
    finally:
        sysexit(0)
