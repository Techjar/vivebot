from discord.ext import commands
import time
import discord
import os

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
        with open(os.environ.get('DATA_DIR') + 'updateprogress.txt', 'w') as file:
            file.write(arg)
        with open(os.environ.get('DATA_DIR') + 'updateversion.txt', 'r') as file:
            fifteenium_version = file.read()
        await ctx.send('`Update query response is now:`\nVivecraft will be updated to MC {0} as soon as possible.\nCurrent progress: {1}'.format(fifteenium_version, arg))

    @commands.command()
    @commands.has_role('Developer')
    async def update(self, ctx, *, arg):
        '''Sets update version'''
        if len(arg) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open(os.environ.get('DATA_DIR') + 'updateversion.txt', 'w') as file:
            file.write(arg)
        with open(os.environ.get('DATA_DIR') + 'updateprogress.txt', 'r') as file:
            progress = file.read()
        await ctx.send('`Update query will respond to {0}, and response is now:`\nVivecraft will be updated to MC {0} as soon as possible.\nCurrent progress: {1}'.format(arg, progress))

def setup(bot):
    bot.add_cog(updateprogress(bot))
