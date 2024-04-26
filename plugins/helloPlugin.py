class Plugin:
    async def execute(self, message):
        raise NotImplementedError

class HelloPlugin(Plugin):
    async def execute(self, message):
        if message.content == "!hi":
            await message.channel.send("Hi !")
