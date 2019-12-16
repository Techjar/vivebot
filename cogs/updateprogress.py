from discord.ext import commands
import time
import discord

class updateprogress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def progress(self, ctx, *args):
        '''Shows the bot\'s latency'''
        if ctx.message.author.id != 147547441170874369 and ctx.message.author.id != 187385331753025536:
            return
        with open('115progress.txt', 'w') as file:
            file.write(" ".join(args))
        await ctx.send('Update progress set to: ' + " ".join(args))

def setup(bot):
    bot.add_cog(updateprogress(bot))
