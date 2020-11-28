#!/usr/bin/env python
import json
import requests
from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get

with open('tokens.json') as json_file:
    token = json.load(json_file)
   
requiredtime = 60000 # in min
adminscfg = "admins.cfg"
class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @commands.guild_only()
    async def whitelist(self, ctx, *, steamid):
        if "ticket" not in str(ctx.channel.name):
            await ctx.author.send("Du kannst nur im Whitelist Ticket die Whitelist beantragen!")

        elif len(steamid) != 17:
            await ctx.send(f""">>> {ctx.author.mention} es ist ein Fehler aufgetreten. Bitte stell sicher, dass du deine Steam64 Id angegeben hast, und deine Spielstunden öffentlich sind! Steam64Id --> https://steamidfinder.com/""")
            

        elif discord.utils.find(lambda r: r.name == 'Whitelist', ctx.message.guild.roles) in ctx.author.roles:
            await ctx.send(f">>> {ctx.author.mention} du scheinst schon auf der Whitelist zustehen. Sollte dies ein Fehler sein, wende dich bitte an den Support")
        elif discord.utils.find(lambda r: r.name == 'WL-Blockiert', ctx.message.guild.roles) in ctx.author.roles:
            await ctx.send(f">>> {ctx.author.mention} du scheinst von der automatisierten Whitelist ausgeschlossen zu sein. Sollte dies ein Fehler sein, wende dich bitte an den Support")

        else:
            try:
                response = requests.get(f"""http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={ token["steam"] }&steamid={steamid}&format=json""")

                data = response.json()["response"]["games"]
            except:
                await ctx.send(f""">>> {ctx.author.mention} es ist ein Fehler aufgetreten. Bitte stell sicher, dass du deine Steam64 Id angegeben hast, und deine Spielstunden öffentlich sind! Steam64Id --> https://steamidfinder.com/""")
           # try:   
           #     with open("data.json", "w") as write_file:
           #         json.dump(data, write_file)
           # except:
           #    print("Error in data dumping")

            try:
                for i in data:
                        if i["appid"] == 393380:
                            playtime = (str(i['playtime_forever']))

                            embed=discord.Embed(title="💌 Whitelist Request", description=f"""{datetime.now().strftime("%c")}""")
                            embed.add_field(name="Nutzername", value=f"{ctx.author.mention}", inline=True)
                            embed.add_field(name="Steam64Id", value=f"{steamid}", inline=True)
                            embed.add_field(name="Squad Stunden", value=f"{round(int(playtime) / 60, 2) }", inline=False)
                            embed.add_field(name="Auto Check", value=f"{int(playtime) >= requiredtime}", inline=True)
                            embed.set_footer(text="GEOBot Steamwhitelist by IMMERVOLL")
                            await ctx.send(embed=embed)
                            break
            except:
                    print("Error in data")
                       
                   
            if int(playtime) >= requiredtime:
                        try:
                            with open(adminscfg, "a") as whitelist:
                                whitelist.write(f"""\nAdmin={steamid}:Whitelist // Playtime : {ctx.author.name} via GEOWhitelist by IMMERVOLL""")
                        
                            print(f"""{datetime.now().strftime("%c")} | Auto Whitelisted {ctx.author.name}:{steamid} with {round(int(playtime) / 60, 2)} hours""")
                            channel = self.bot.get_channel(781158188111495219)
                            await channel.send(f"""{datetime.now().strftime("%c")} | Auto Whitelisted {ctx.author.mention}:{steamid} with {round(int(playtime) / 60, 2)} hours""")
                            await ctx.send("Added to Whitelist") 
                            await ctx.message.author.add_roles(discord.utils.get(ctx.message.author.guild.roles, name="Whitelist")) 
                        except: 
                            print("Error in index CFG")
                           

    @commands.command()
    async def squadtime(self, ctx, *, steamid):
        if len(steamid) != 17:
            await ctx.send(f""">>> {ctx.author.mention} es ist ein Fehler aufgetreten. Bitte stell sicher, dass du deine Steam64 Id angegeben hast, und deine Spielstunden öffentlich sind! Steam64Id --> https://steamidfinder.com/""")
            
        
        else:
            try:
                response = requests.get(f"""http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={ token["steam"] }&steamid={steamid}&format=json""")

                data = response.json()["response"]["games"]
            except:
                await ctx.send(f""">>> {ctx.author.mention} es ist ein Fehler aufgetreten. Bitte stell sicher, dass du deine Steam64 Id angegeben hast, und deine Spielstunden öffentlich sind! Steam64Id --> https://steamidfinder.com/""")
            try:   
                with open("data.json", "w") as write_file:
                    json.dump(data, write_file)
            except:
                print("Error in data dumping")

            try:
                for i in data:
                        if i["appid"] == 393380:
                            playtime = (str(i['playtime_forever']))

                            embed=discord.Embed(title="🎮 Squadtime", description=f"""{datetime.now().strftime("%c")}""")
                            embed.add_field(name="Steam64Id", value=f"{steamid}", inline=True)
                            embed.add_field(name="Squad Stunden", value=f"{round(int(playtime) / 60, 2) }", inline=False)
                            embed.set_footer(text="GEOBot Steamwhitelist by IMMERVOLL")
                            await ctx.send(embed=embed)
                            break
            except:
                    print("Error in data")
                       
                   
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Admin", "Techniker")
    async def adminwl(self, ctx, member : discord.Member, *, steamid):
        if "ticket" not in str(ctx.channel.name):
            await ctx.author.send("Du kannst nur im Whitelist Ticket die Whitelist beantragen!")

        elif len(steamid) != 17:
            await ctx.send(f""">>> {ctx.author.mention} es ist ein Fehler aufgetreten. Bitte stell sicher, dass du eine Steam64 Id angegeben hast, und die Spielstunden öffentlich sind! Steam64Id --> https://steamidfinder.com/""")
            

        elif discord.utils.find(lambda r: r.name == 'Whitelist', ctx.message.guild.roles) in member.roles:
            await ctx.send(f">>> {ctx.author.mention} das Ziel {member.mention} steht schon auf der Whitelist")
        elif discord.utils.find(lambda r: r.name == 'WL-Blockiert', ctx.message.guild.roles) in ctx.author.roles:
            await ctx.send(f">>> {ctx.author.mention} das Ziel {member.mention} wurde von der automatisierten Whitelist ausgeschlossen.")

        else:
                        try:
                            with open(adminscfg, "a") as whitelist:
                                whitelist.write(f"""\nAdmin={steamid}:Whitelist // Manually : {member.name} via GEOWhitelist by IMMERVOLL""")
                        
                            print(f"""{datetime.now().strftime("%c")} | Auto Whitelisted {member.name}:{steamid} with manually by {ctx.author.name}""")
                            channel = self.bot.get_channel(781158188111495219)
                            await channel.send(f"""{datetime.now().strftime("%c")} | Auto Whitelisted {member.mention}:{steamid} manually by {ctx.author.mention}""")
                            await ctx.send("Added to Whitelist") 
                            await member.add_roles(discord.utils.get(member.guild.roles, name="Whitelist")) 
                        except: 
                            print("Error in index CFG")

    @adminwl.error
    async def adminwl_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Du hast keine Macht über mich")
                    
    @commands.guild_only()
    @commands.has_any_role("Admin", "Techniker")
    @commands.command(hidden=True)
    async def purge(self, ctx, *, msg : int):
        await ctx.message.channel.purge(limit= msg+1)
def setup(bot):
    bot.add_cog(Whitelist(bot))
   
    