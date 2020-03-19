from discord.ext import commands
import time
import discord

class updateprogress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Developer')
    async def progress(self, ctx, *, arg):
        '''Sets update progress'''
        if len(arg) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateprogress.txt', 'w') as file:
            file.write(arg)
        await ctx.send('Update progress set to: ' + arg)

    @commands.command()
    @commands.has_role('Developer')
    async def update(self, ctx, *, arg):
        '''Sets update version'''
        if len(arg) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateversion.txt', 'w') as file:
            file.write(arg)
        await ctx.send('Update version set to: ' + arg)

def setup(bot):
    bot.add_cog(updateprogress(bot))
