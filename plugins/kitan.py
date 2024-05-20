"""

kitan plugin

"""

import discord, requests, random, re
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

has = ConfigParser()

class kitan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class kitanDropdown(discord.ui.Select):
        def __init__(self):
            option=[
                discord.SelectOption(label="Games", description="Extra games for Miyuchan"),
                discord.SelectOption(label="Roles", description="Placeholder")
            ]
            super().__init__(placeholder="In which domain do you need help with ?", options=option, min_values=1, max_values=1)
        
        async def callback(self, i: discord.Interaction):
            embed = discord.Embed(title=self.values[0], description='`kitan` is a plugin made for fun. Prefix `-`', color=discord.Color.yellow())
            embed.set_thumbnail(url="https://raw.githubusercontent.com/yuaself/img-host/main/konoyuzu.png")
            embed.set_footer(text="kitan", icon_url="https://raw.githubusercontent.com/yuaself/img-host/main/konoyuzu.png")

            if self.values[0] == 'Games':
                embed.add_field(name="-number number points", value='Bet on a number between 1 and 4.', inline=False)
                embed.add_field(name="-rps rock/paper/scissors points", value='Play the traditional game of Rock-Paper-Scissors.', inline=False)
                
            if self.values[0] == 'Roles':                        
                embed.add_field(name="", value="", inline=False)

            await i.response.send_message(embed=embed, ephemeral=True)
        
    class kitanView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(kitan.kitanDropdown())

    @commands.Cog.listener("on_message")
    async def kitan_commands(self, message):
        has.read('server_config.ini')
        if message.author.id == self.bot.user.id:
            return
        if "kitan" in has.get(str(message.author.guild.id), 'plugins'):
            if message.content == "-kitan":
                await message.channel.send("Here you go for the **kitan** plugin :",view=kitan.kitanView())
            
            if message.content.startswith("-number"):
                match = re.search(r'-number (\d+) (\d+)', message.content)
                user_data = has[str(message.author.guild.id)]
                info = user_data[str(message.author.id)]
                listing = info.split()
                lvl_user_db =  int(listing[0])
                warn_user_db = int(listing[2])
                xp_user_db = int(listing[1])
                points_user_db = int(listing[3])
                claim_debut = int(listing[4])
                random_number = random.randint(1,4)
                if match:
                    chosen_number = int(match.group(1))
                    points_bet = int(match.group(2))
                    if chosen_number > 4 or chosen_number < 1:
                        await message.channel.send(f"Oops! It seems there was an error while doing the command, try to match `-number number(from 1 to 4) points`:confused:")

                    elif chosen_number == random_number:
                        embed = discord.Embed(title=f"You guessed it right {message.author.display_name}!", description=f"You won +{points_bet*3} Points!", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db += points_bet*3
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
                    else:
                        embed = discord.Embed(title=f"Oh... You guessed it wrong {message.author.display_name}!", description=f"You lost {points_bet} Points...", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db -= points_bet
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
                else:
                    await message.channel.send(f"Oops! It seems there was an error while doing the command, try to match `-number number(from 1 to 4) points`:confused:")
            
            if message.content.startswith("-rps"):
                match = re.search(r'-rps (rock|paper|scissors) (\d+)', message.content)
                user_data = has[str(message.author.guild.id)]
                info = user_data[str(message.author.id)]
                listing = info.split()
                lvl_user_db =  int(listing[0])
                warn_user_db = int(listing[2])
                xp_user_db = int(listing[1])
                points_user_db = int(listing[3])
                claim_debut = int(listing[4])
                random_rps = random.choice(["rock", "paper", "scissors"])
                if match:
                    hand = str(match.group(1)).lower()
                    points_bet = int(match.group(2))
                    if hand not in ["rock", "paper", "scissors"]:
                        await message.channel.send(f"Oops! It seems there was an error while doing the command, try to match `-rps rock/paper/scissors points` :confused:")

                    elif hand == "rock" and random_rps == "scissors":
                        embed = discord.Embed(title=f"You won {message.author.display_name}!", description=f"You won +{points_bet} Points!", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db += points_bet*2
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
                    elif hand == "paper" and random_rps == "rock":
                        embed = discord.Embed(title=f"You won {message.author.display_name}!", description=f"You won +{points_bet} Points!", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db += points_bet*2
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
                    elif hand == "scissors" and random_rps == "paper":
                        embed = discord.Embed(title=f"You won {message.author.display_name}!", description=f"You won +{points_bet} Points!", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db += points_bet*2
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
                    elif hand == random_rps:
                        embed = discord.Embed(title=f"It's a tie {message.author.display_name}!", description=f"No points were given!", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title=f"You lost {message.author.display_name}...", description=f"You lost {points_bet} Points", color=discord.Color.yellow())
                        await message.channel.send(embed=embed)
                        points_user_db -= points_bet
                        has.set(str(message.author.guild.id), str(message.author.id), f"{lvl_user_db} {xp_user_db} {warn_user_db} {points_user_db} {claim_debut} 0 0 0 0 0 0 0")
                        with open('server_config.ini', 'w') as f:
                            has.write(f)
        
                else:
                    await message.channel.send(f"Oops! It seems there was an error while doing the command, try to match `-rps rock/paper/scissors points` :confused:")
            

async def setup(bot):
    await bot.add_cog(kitan(bot))
