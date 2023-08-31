from discord.ext import commands
import discord
from aiohttp_requests import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys
import traceback
import re
from packaging import version

class faq(commands.Cog, name='FAQ'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['questions', 'issue', 'issues'])
    async def faq(self, ctx, *args):
        '''Displays jumpable buttons to the FAQ or a specific entry from the FAQ'''
        if len(args) == 0:
            embed = discord.Embed(title=" ", color=0x82f4f4)
            embed.set_author(name="FAQ - Jump To:", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
            embed.add_field(name="Gameplay", value="http://www.vivecraft.org/faq/#gameplay", inline=True)
            embed.add_field(name="Compatibility", value="http://www.vivecraft.org/faq/#compatibility", inline=True)
            embed.add_field(name="Troubleshooting", value="http://www.vivecraft.org/faq/#troubleshooting", inline=True)
            embed.set_footer(text="ping @shay#0038 or @Techjar#3305 if you have any issues!")
            await ctx.send(embed=embed)
        else:
            async with ctx.channel.typing():
                try:
                    response = await requests.get("http://www.vivecraft.org/faq/", timeout=5)
                    resp_text = await response.text()
                    html = BeautifulSoup(resp_text, "html.parser")
                    root = html.find("div", {"class": "entry-content"})
                    
                    desc = ""
                    image = None
                    found = False
                    for mode in range(0, 2):
                        if found:
                            break
                        for element in root.find_all("div", recursive=False):
                            title_element = element.find("blockquote")
                            if title_element is not None and ((mode == 0 and element.attrs['id'] == args[0].lower()) or (mode == 1 and " ".join(args).lower() in title_element.find("p").text.lower())):
                                id = element.attrs['id']
                                title = title_element.find("p").text
                                for part in element.find_all(True, recursive=False):
                                    if part.name == "p":
                                        if image is None:
                                            for img in part.find_all("img"):
                                                image = img.attrs['src']
                                                break
                                        
                                        if not part.text.strip():
                                            continue
                                        for tag in part.contents:
                                            if isinstance(tag, NavigableString):
                                                desc += tag
                                            elif tag.name == "a":
                                                link = tag.attrs['href']
                                                if not re.match(r'^[a-z0-9]+://', link, re.IGNORECASE):
                                                    if link.startswith("/"):
                                                        link = "http://www.vivecraft.org" + link
                                                    else:
                                                        link = "http://www.vivecraft.org/faq/" + link
                                                desc += "[" + tag.text + "](" + link + ")"
                                            elif tag.name == "strong":
                                                desc += "**" + tag.text + "**"
                                            elif tag.name == "i":
                                                desc += "*" + tag.text + "*"
                                            else:
                                                desc += tag.text
                                        desc += "\n\n"
                                    elif part.name == "ul":
                                        for item in part.find_all("li"):
                                            desc += "• " + item.text.strip() + "\n"
                                        desc += "\n"
                                    elif part.name == "ol":
                                        for i, item in enumerate(part.find_all("li")):
                                            desc += str(i + 1) + ". " + item.text.strip() + "\n"
                                        desc += "\n"
                                found = True
                                break
                            
                    #print(desc)
                    
                    # Unused code to list all issues. Too spammy!
                    #for element in root.find_all("div", recursive=False):
                    #    title_element = element.find("blockquote")
                    #    if title_element is not None:
                    #        desc += "**" + element.attrs['id'] + "** - "
                    #        title = title_element.find("p").text
                    #        desc += ((title[:40] + "..") if len(title) > 40 else title) + "\n"
                    
                    if found:
                        embed = discord.Embed(title="", description=desc, color=0x82f4f4)
                        embed.set_author(name="FAQ - " + title, url="http://www.vivecraft.org/faq/#" + id,
                                        icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
                        embed.add_field(name="For more questions see the full FAQ", value="http://www.vivecraft.org/faq/", inline=True)
                        if image is not None:
                            embed.set_image(url=image)
                        if ctx.message.reference is not None:
                            await ctx.send(embed=embed, reference=ctx.message.reference)
                            await ctx.message.delete()
                        else:
                            await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title="An error occurred", description="Please report this to @Techjar#3305", color=0xff0000)
                    await ctx.send(embed=embed)
                    traceback.print_exc()

    @commands.command(aliases=['download', 'dl'])
    async def downloads(self, ctx):
        '''Embed download links'''
        try:
            response = await requests.get("http://www.vivecraft.org/downloads/", timeout=5)
            resp_text = await response.text()
            html = BeautifulSoup(resp_text, "html.parser")
            table = html.find("table")
            rows = table.find_all("tr")
            
            versions = []
            for cell in rows[0].find_all("th")[1:]:
                versions.append({'name': cell.text})
            
            def find_urls(row, key):
                span_acc = 0
                for idx, cell in enumerate(rows[row].find_all("td")[1:]):
                    link = cell.find("a")
                    if link is not None:
                        span = int(cell.attrs['colspan']) if 'colspan' in cell.attrs else 1
                        for i in range(0, span):
                            versions[idx + span_acc + i][key] = link.attrs['href']
                        span_acc += span - 1
            
            find_urls(2, 'client_url')
            #find_urls(4, 'spigot_url')
            #find_urls(5, 'forge_url')
            
            response = await requests.get("https://api.modrinth.com/v2/project/vivecraft/version?loaders=[%22fabric%22]", timeout=5)
            modrinth_data = await response.json()
            
            modrinth_ver = "0.0.0"
            for ent in modrinth_data:
                try:
                    if version.parse(ent['game_versions'][-1]) > version.parse(modrinth_ver):
                        modrinth_ver = ent['game_versions'][-1]
                except version.InvalidVersion:
                    pass
            
            embed = discord.Embed(title="", description="Installation instructions can be found at [vivecraft.org/downloads](http://www.vivecraft.org/downloads/). All download links can also be found there, including discontinued legacy versions.", color=0x5e9d34)
            embed.set_author(name="Downloads", url="http://www.vivecraft.org/downloads/", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
            for ver in versions:
                field_desc = "[VR & Non-VR Client](" + ver['client_url'] + ")"
                #if 'spigot_url' in ver:
                #    field_desc += "\n[Spigot Server Plugin](" + ver['spigot_url'] + ")"
                #if 'forge_url' in ver:
                #    field_desc += "\n[Forge Server Mod](" + ver['forge_url'] + ")"
                embed.add_field(name=ver['name'] + " Standalone", value=field_desc, inline=True)
            embed.add_field(name=modrinth_ver + " Mod", value="[Modrinth](https://modrinth.com/mod/vivecraft)\n[CurseForge](https://www.curseforge.com/minecraft/mc-mods/vivecraft)", inline=True)
            embed.add_field(name="Server Plugins", value="[Spigot Server Plugin](https://github.com/jrbudda/Vivecraft_Spigot_Extensions/releases)\n[Forge Server Mod](https://www.curseforge.com/minecraft/mc-mods/vivecraft-forge-extensions/files)", inline=True)
            
            if ctx.message.reference is not None:
                await ctx.send(embed=embed, reference=ctx.message.reference)
                await ctx.message.delete()
            else:
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="An error occurred", description="Please report this to @Techjar#3305", color=0xff0000)
            await ctx.send(embed=embed)
            traceback.print_exc()

    @commands.command()
    async def forum(self, ctx):
        '''Link to the forum'''
        embed = discord.Embed(title=" ", color=0x82f4f4)
        embed.set_author(name="Forum - Jump To:", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        embed.add_field(name="Main Page", value="http://www.vivecraft.org/forum/", inline=True)
        embed.add_field(name="General", value="http://www.vivecraft.org/forum/viewforum.php?f=6", inline=True)
        embed.add_field(name="Troubleshooting", value="http://www.vivecraft.org/forum/viewforum.php?f=3", inline=True)
        embed.add_field(name="Multiplayer", value="http://www.vivecraft.org/forum/viewforum.php?f=4", inline=True)
        embed.add_field(name="Modpacks", value="http://www.vivecraft.org/forum/viewforum.php?f=7", inline=True)
        embed.set_footer(text="ping @shay#0038 or @Techjar#3305 if you have any issues!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(faq(bot))
