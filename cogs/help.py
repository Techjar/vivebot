from discord.ext import commands
from discord.ext.commands import has_permissions
import discord

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(add_reactions=True, embed_links=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands."""
        try:
            if not cog:
                #botname = self.bot.name
                embed = discord.Embed(title='President Obama Help Menu', description='Use `?help <cog>` to find out more!')
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                embed.add_field(name='List of Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                embed.set_footer(text="ping @shay#0038 if you have any issues!")
                await ctx.send(embed=embed)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            embed=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    embed.add_field(name=c.name,value=c.help,inline=False)
                            found = True
                if not found:
                    embed = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                else:
                    await ctx.send(embed=embed)
        except:
            pass

def setup(bot):
    bot.add_cog(help(bot))
