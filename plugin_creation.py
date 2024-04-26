confirm = False

while confirm != True:
    print("Names with spaces are replaced, from 'Beautiful Plugin' to 'BeautifulPlugin' ")
    PLUGIN_NAME = str(input("Plugin name: ")).replace(' ', '')
    PLUGIN_AUTHOR = str(input("Plugin author: "))
    CONFIRM = str(input(f"NAME: {PLUGIN_NAME} | AUTHOR: {PLUGIN_AUTHOR}\nConfirm ? y/n\n"))
    if CONFIRM.lower() == 'y':
        confirm = True

template = f"""
'''
{PLUGIN_NAME} by {PLUGIN_AUTHOR}
'''
import discord, requests
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

cfg = ConfigParser()

class {PLUGIN_NAME}(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def {PLUGIN_NAME.lower()}_commands(self, message):
        cfg.read('server_config.ini')
        if "{PLUGIN_NAME}" in cfg.get(str(message.author.guild.id), 'plugins'):
            # Your commands go here
            if message.content == "!world":
                await message.channel.send("Hello world!")

async def setup(bot):
    await bot.add_cog({PLUGIN_NAME}(bot))
"""

with open(f"{PLUGIN_NAME}.py", 'w') as file:
    file.write(template)

app_exit = str(input("Plugin file created!"))