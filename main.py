from traceback import format_exception
from os import chdir, path
from argparse import ArgumentParser
from discord.ext import commands

from cogs.utils.logger import Logger
from cogs.utils.config import Config

logger = Logger(__name__)

__VERSION_NUMBER__ = (0, 1, 0)
__VERSION__ = ".".join([str(y) for y in __VERSION_NUMBER__])

_startup_msg = "Starting Nukebot Version {0}".format(__VERSION__)
print(_startup_msg)
logger.info(_startup_msg)

directory = path.dirname(path.realpath(__file__))
chdir(directory)

def parse_cmd_arguments():  # allows for arguments
    parser = ArgumentParser(description="nukebot")
    parser.add_argument("--reset-config",  # Allows for Testing of mac related code
                        action="store_true",
                        help="Reruns the setup")
    return parser

args = parse_cmd_arguments().parse_args()

def setup():

    print("Setup Process\n\nToken\n")
    config.token = input(">")

    print("Prefix\n")
    config.prefix = input(">").split(" ")

    config.save()
    return


config = Config("config", {"token": "", "prefix": []})
if not config.token or args.reset_config:
    setup()

bot = commands.Bot(command_prefix=config.prefix)


@bot.check_once
def whitelist(ctx):
    if ctx.message.author == bot.owner:
        return True

    if ctx.message.author.id in bot.allowedusers.id:
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
        logger.warn(exception_log)


@bot.event
async def on_ready():
    application = await bot.application_info()
    bot.owner = application.owner

    bot.allowedusers = Config("allowedusers", {"id": []})

    addons = Config("addons", {'loaded': []})
    # Notify user if an addon fails to load.
    for addon in addons.loaded:
        try:
            bot.load_extension(addon)
        except Exception as e:
            logger.warn("Failed to load {}:\n{}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))

    if bot.guilds:
        print("\nClient logged in as {}, in the following guild(s):".format(
            bot.user.name))
        for guild in bot.guilds:
            print(guild.name)
    else:
        print("\nClient logged in as {}, in no guilds".format(bot.user.name))


if __name__ == "__main__":
    try:
        bot.run(config.token)
    except KeyboardInterrupt:
        bot.logout()
