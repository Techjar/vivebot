from discord.ext import commands
import time
import discord

class updateprogress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Developer')
    async def progress(self, ctx, *args):
        '''Sets update progress'''
        if len(args) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateprogress.txt', 'w') as file:
            file.write(" ".join(args))
        await ctx.send('Update progress set to: ' + " ".join(args))

    @commands.command()
    @commands.has_role('Developer')
    async def update(self, ctx, *args):
        '''Sets update version'''
        if len(args) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateversion.txt', 'w') as file:
            file.write(" ".join(args))
        await ctx.send('Update version set to: ' + " ".join(args))

def setup(bot):
    bot.add_cog(updateprogress(bot))
