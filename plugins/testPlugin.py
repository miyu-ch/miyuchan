import discord, requests
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()

class testPlugin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def testplugin_commands(self, message):
        has.read('server_config.ini')
        if "testPlugin" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == "!test":
                await message.channel.send("Testing")
            
async def setup(bot):
    await bot.add_cog(testPlugin(bot))
