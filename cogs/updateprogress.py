from discord.ext import commands
import time
import discord

class updateprogress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def progress(self, ctx, *args):
        '''Sets update progress'''
        if ctx.message.author.id != 147547441170874369 and ctx.message.author.id != 187385331753025536:
            return
        if len(args) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateprogress.txt', 'w') as file:
            file.write(" ".join(args))
        await ctx.send('Update progress set to: ' + " ".join(args))

    @commands.command()
    async def update(self, ctx, *args):
        '''Sets update version'''
        if ctx.message.author.id != 147547441170874369 and ctx.message.author.id != 187385331753025536:
            return
        if len(args) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open('updateversion.txt', 'w') as file:
            file.write(" ".join(args))
        await ctx.send('Update version set to: ' + " ".join(args))

def setup(bot):
    bot.add_cog(updateprogress(bot))
