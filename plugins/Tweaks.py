import discord, requests, random
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()

class Tweaks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class tweaksDropdown(discord.ui.Select):
        def __init__(self):
            option=[
                discord.SelectOption(label="Server", description="Placeholder"),
                discord.SelectOption(label="Roles", description="Placeholder")
            ]
            super().__init__(placeholder="In which domain do you need help with ?", options=option, min_values=1, max_values=1)
        
        async def callback(self, i: discord.Interaction):
            embed = discord.Embed(title=self.values[0], description='The `Tweaks` plugin (Official Miyuchan plugin) is more of a technical plugin for Miyuchan. It may not have a lot of features, it is mostly for showcasing.', color=discord.Color.magenta())
            embed.set_thumbnail(url="https://raw.githubusercontent.com/yuaself/img-host/main/76f13ec315998f61104ffe20fae276d4.webp")
            embed.set_footer(text="Tweaks by the Miyuchan team")

            if self.values[0] == 'Server':
                embed.add_field(name="", value='Prefix `.`', inline=False)
                embed.add_field(name="server-info", value='Get current server basic information', inline=False)
                embed.add_field(name="server-config (Administrator permission)", value="Get current server Miyuchan's configuration", inline=False)
                embed.add_field(name="server-roles", value="Show server's roles", inline=False)
            if self.values[0] == 'Roles':                        
                embed.add_field(name="server-roles", value="Show server's roles", inline=False)
                embed.add_field(name="role @role", value="Get information from a role", inline=False)
            await i.response.send_message(embed=embed, ephemeral=True)
        
    class tweaksView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(Tweaks.tweaksDropdown())

    @commands.Cog.listener("on_message")
    async def tweaks_commands(self, message):
        global target_word
        has.read('server_config.ini')
        if message.author.id == self.bot.user.id:
            return
        if "Tweaks" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == ".tweaks":
                await message.channel.send("Here you go for the **Tweaks** plugin :",view=Tweaks.tweaksView())
            if message.content == ".server-info":
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
            if message.content == ".server-config":
                if message.author.guild_permissions.administrator:
                    configuration = f"```ini\n[{message.author.guild.id}]"
                    for values in has.options(str(message.author.guild.id)):
                        try:
                            int(values)
                        except:
                            text = f"{values}: ",has.get(str(message.author.guild.id), values)
                            print(text)
                            configuration += f"\n{text}"
                    configuration = configuration.replace("(", '').replace(")",'').replace("'","").replace(",",'').replace("  ",' ')
                    await message.channel.send(f"**{message.author.guild.name}'s config**:\n{configuration}```")
                else:
                    await message.channel.send("Oops! You don't have the **Administrator** permission! :confused:")
            if message.content == ".server-roles":
                roles = message.author.guild.roles
                role_list = "\n".join([role.name for role in roles])
                await message.channel.send(role_list)
            if message.content.startswith(".role"):
                try:
                    role = message.role_mentions[0]
                    enabled_perms = [perm for perm, value in role.permissions if value]
                    embed = discord.Embed(title=f'Role Information - {role.name}', color=role.color)
                    embed.add_field(name='Role ID:', value=role.id, inline=False)
                    embed.add_field(name='Members:', value=len(role.members), inline=False)
                    embed.add_field(name='Position:', value=role.position, inline=False)
                    embed.add_field(name='Mentionable:', value=role.mentionable, inline=False)
                    embed.add_field(name='Hoist:', value=role.hoist, inline=False)
                    embed.add_field(name='Managed:', value=role.managed, inline=False)
                    embed.add_field(name='Enabled Permissions:', value=', '.join(enabled_perms) if enabled_perms else 'No enabled permissions', inline=False)
                    await message.channel.send(embed=embed)
                except IndexError:
                    await message.channel.send("Oops! It seems you didn't mention the role to get info from :confused:")         

async def setup(bot):
    await bot.add_cog(Tweaks(bot))
