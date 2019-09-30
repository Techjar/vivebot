from discord.ext import commands
import time
import discord

class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''Shows the bot\'s latency'''
        pingprior=time.monotonic()
        ping = discord.Embed(title='Pong! :ping_pong:', description='```xl\nBeep Boop, waiting to finish...```')
        message=await ctx.send(embed=ping)
        ping=(time.monotonic() - pingprior) * 1000
        pong = discord.Embed(title='Pong! :ping_pong:', description=f'```xl\n{int(ping)}ms    ```')
        await message.edit(embed=pong)#content=f"Pong!  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

    @commands.command()
    async def info(self, ctx):
        '''Bot info. may do server info later idk'''
        infbed = discord.Embed(title='🖥 ViveBot Info', description=' ', color=0x96c6fa)
        infbed.add_field(name='📚 Library', value='`Discord.py`', inline=True)
        infbed.add_field(name='📤 Version', value='`Vivebot v0.1`', inline=True)
        infbed.set_footer(text='Created by shay#0038 (115238234778370049)')
        await ctx.send(embed=infbed)

def setup(bot):
    bot.add_cog(system(bot))
