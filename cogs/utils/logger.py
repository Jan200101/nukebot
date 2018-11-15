from datetime import date, datetime
from sys import _getframe
from asyncio import ensure_future
from discord import Embed, Color
from discord.errors import Forbidden
from cogs.utils.formatting import escape
from discord.channel import TextChannel


class Logger:

    def __init__(self, name, channel=None, *, dateform="%d/%m/%Y %H:%M"):
        self.name = name
        if channel and channel.__class__ != TextChannel:
            raise TypeError("channel argument is not of type TextChannel")
        self.channel = channel
        self.dateform = dateform

    def write(self, content, type, function):
        time = datetime.now().strftime(self.dateform)
        with open("logs/{}.log".format(str(date.today())), "a") as file:
            file.write("[{time}] {type} {name} {function}: {content}\n".format(
                time=time, type=type, name=self.name, function=function, content=content))

    async def send(self, content, type, function, color):
        emb = Embed(color=color)
        (emb.add_field(name="Type", value=type)
            .add_field(name="Name", value=escape(self.name))
            .add_field(name="Function", value=escape(function))
            .add_field(name="Message", value=escape(content), inline=True))
        try:
            await self.channel.send(embed=emb)
        except Forbidden:
            await self.channel.send("{type} {name} {function}: {content}\n".format(type=type, name=self.name, function=function, content=content))

    def info(self, content):
        type = "INFO"
        function = _getframe(1).f_code.co_name
        self.write(content, type, function)
        if self.channel:
            ensure_future(self.send(content, type, function, Color.green()))

    def warn(self, content):
        type = "WARNING"
        function = _getframe(1).f_code.co_name
        print("[{function}] {content}".format(
            function=function, content=content))
        self.write(content, type, function)
        if self.channel:
            ensure_future(self.send(content, type, function, Color.red()))
