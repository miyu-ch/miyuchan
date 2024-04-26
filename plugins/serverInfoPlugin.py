import discord, requests
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()

class serverInfoPlugin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def serverinfoplugin_commands(self, message):
        has.read('server_config.ini')
        if "serverInfoPlugin" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == "!serverinfo":
                server = message.author.guild
                roles_count = len(server.roles)
                channels_count = len(server.channels)
                members_count = server.member_count
                created_at = server.created_at.strftime("%B %d, %Y")

                embed = discord.Embed(title="Server Information", color=discord.Color.blurple())
                embed.set_thumbnail(url=server.icon)
                embed.add_field(name="Server Name", value=server.name, inline=False)
                embed.add_field(name="Server ID", value=server.id, inline=False)
                embed.add_field(name="Owner", value=server.owner.display_name, inline=True)
                embed.add_field(name="Members Count", value=members_count, inline=True)
                embed.add_field(name="Roles Count", value=roles_count, inline=True)
                embed.add_field(name="Channels Count", value=channels_count, inline=True)
                embed.add_field(name="Creation Date", value=created_at, inline=True)
                await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(serverInfoPlugin(bot))