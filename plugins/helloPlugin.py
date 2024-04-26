import discord, requests
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()

class helloPlugin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def helloplugin_commands(self, message):
        has.read('server_config.ini')
        if "helloPlugin" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == "!helloplugin":
                embed = discord.Embed(title="Hello Plugin", description='A simple plugin saying hello', color=discord.Color.blurple())
                embed.add_field(name="!helloplugin", value="Showing all commands in the Hello Plugin", inline=False)
                embed.add_field(name="!hi", value="Saying hi", inline=False)
                await message.channel.send(embed=embed)
            if message.content == "!hi":
                await message.channel.send("Hi")
            
async def setup(bot):
    await bot.add_cog(helloPlugin(bot))


