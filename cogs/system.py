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
        ping = discord.Embed(title='Pong! :ping_pong:', description='```xl\n<:vive:273632415627476992> Waiting to finish...```')
        message=await ctx.send(embed=ping)
        ping=(time.monotonic() - pingprior) * 1000
        pong = discord.Embed(title='Pong! :ping_pong:', description=f'```xl\n{int(ping)}ms    ```')
        await message.edit(embed=pong)#content=f"Pong!  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

    @commands.command()
    async def info(self, ctx):
        '''Bot info. may do server info later idk'''
        infbed = discord.Embed(title='🖥 Info', description=' ', color=0x96c6fa)
        infbed.add_field(name='📚 Library', value='`Discord.py`', inline=True)
        infbed.add_field(name='<:vive:273632415627476992> Version', value='`v0.1`', inline=True)
        infbed.set_footer(text='Created by shay#0038 (115238234778370049)')
        await ctx.send(embed=infbed)
        
    @commands.command()
    async def tester(self, ctx):
        '''Assign/remove tester role'''
        role = discord.utils.get(ctx.guild.roles, name="Tester")
        try:
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send('You are no longer in the tester group.')
            else:
                await ctx.author.add_roles(role)
                await ctx.send('You are now in the tester group.')
        except discord.Forbidden:
            await ctx.send('I am unable to change your role, citizen.')

    #I'm not sure if this can be run if you're not the bot owner, so i've disabled it for now
    """@commands.command()
                async def shutdown(self, ctx):
                    '''Shuts down'''
                    await ctx.send('<:vive:273632415627476992> Shutting down.')
                    await ctx.bot.close()"""

def setup(bot):
    bot.add_cog(system(bot))
