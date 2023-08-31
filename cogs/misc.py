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

async def setup(bot):
    await bot.add_cog(misc(bot))
