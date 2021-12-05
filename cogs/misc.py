from discord.ext import commands
import time
import discord

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tester(self, ctx):
        '''Assign/remove tester role'''
        role = discord.utils.get(ctx.guild.roles, name="Tester")
        try:
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send('Thanks, {}. You are no longer in the tester group.'.format(discord.utils.escape_mentions(ctx.author.name)))
            else:
                await ctx.author.add_roles(role)
                await ctx.send('You are now in the tester group. Welcome aboard, {}.'.format(discord.utils.escape_mentions(ctx.author.name)))
        except discord.Forbidden:
            await ctx.send('I am unable to change your role, citizen.')

    @commands.command(aliases=['download', 'dl'])
    async def downloads(self, ctx):
        '''Embed download links'''
        embed = discord.Embed(title="", description="Download links for all versions of Vivecraft, as well as server-side plugins and mods, can be found at [vivecraft.org/downloads](http://www.vivecraft.org/downloads/). There is a couple of nicely laid out tables for currently supported and discontinued versions.", color=0x4287d7)
        embed.set_author(name="Downloads", url="http://www.vivecraft.org/downloads/", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        if ctx.message.reference is not None:
            await ctx.send(embed=embed, reference=ctx.message.reference)
            await ctx.message.delete()
        else:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))
