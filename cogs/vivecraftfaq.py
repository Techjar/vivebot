from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys
import traceback

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
            try:
                response = requests.get("http://www.vivecraft.org/faq/", timeout=3)
                html = BeautifulSoup(response.text, "html.parser")
                root = html.find("div", {"class": "entry-content"})
                
                desc = ""
                title = None
                image = None
                for mode in range(0, 2):
                    for element in root.find_all("div", recursive=False):
                        title_element = element.find("blockquote")
                        if title_element is not None and ((mode == 0 and element.attrs['id'] == args[0]) or (mode == 1 and " ".join(args).lower() in title_element.find("p").text.lower())):
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
                                            desc += "[" + tag.text + "](" + tag.attrs['href'] + ")"
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
                            break
                
                # Unused code to list all issues. Too spammy!
                #for element in root.find_all("div", recursive=False):
                #    title_element = element.find("blockquote")
                #    if title_element is not None:
                #        desc += "**" + element.attrs['id'] + "** - "
                #        title = title_element.find("p").text
                #        desc += ((title[:40] + "..") if len(title) > 40 else title) + "\n"
                
                if title is not None:
                    embed = discord.Embed(title="", description=desc, color=0x82f4f4)
                    embed.set_author(name="FAQ - " + title, url="http://www.vivecraft.org/faq/#" + id,
                                    icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
                    embed.add_field(name="For more questions see the full FAQ", value="http://www.vivecraft.org/faq/", inline=True)
                    if image is not None:
                        embed.set_image(url=image)
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
        embed.add_field(name="General", value="http://www.vivecraft.org/forum/viewforum.php?f=6&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Troubleshooting", value="http://www.vivecraft.org/forum/viewforum.php?f=3&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Multiplayer", value="http://www.vivecraft.org/forum/viewforum.php?f=4&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Modpacks", value="http://www.vivecraft.org/forum/viewforum.php?f=7&sid=86d1ec6bd700699b3484b5083bbb6da4", inline=True)
        embed.set_footer(text="ping @shay#0038 or @Techjar#3305 if you have any issues!")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(faq(bot))
