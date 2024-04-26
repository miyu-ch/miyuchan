import discord, requests
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()
has.read('server_config.ini')

class testPlugin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def testplugin_commands(self, message):
        if "helloPlugin" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == "!test":
                await message.channel.send("Testing")
            
async def setup(bot):
    await bot.add_cog(testPlugin(bot))


