from discord.ext import commands
import time
import discord
import re

class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''Shows the bot\'s latency'''
        pingprior=time.monotonic()
        ping = discord.Embed(title='Pong! :ping_pong:', description='```xl\n<:vive:683522338331033601> Waiting to finish...```')
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
        infbed.add_field(name='<:vive:683522338331033601> Version', value='`v0.1`', inline=True)
        infbed.set_footer(text='Created by shay#0038 (115238234778370049)')
        await ctx.send(embed=infbed)

    @commands.command()
    @commands.has_role('Developer')
    async def say(self, ctx, *args):
        '''Make the bot say something'''
        if ctx.message.channel_mentions:
            await ctx.message.channel_mentions[0].send(' '.join(args[1:]))
        else:
            await ctx.send('You need to specify a channel, sir.')

    @commands.command()
    @commands.has_role('Developer')
    async def react(self, ctx, *args):
        '''Make the bot say something'''
        if len(args) >= 2:
            msg = await ctx.fetch_message(int(args[0]))
            if msg is not None:
                res = re.search(':(.*):', args[1])
                if res is not None:
                    emoji = discord.utils.get(self.bot.emojis, name=res.group(1))
                    if emoji is not None:
                        await msg.add_reaction(emoji)
                    else:
                        await ctx.send('That emoji is invalid.')
                else:
                    await msg.add_reaction(args[1])
            else:
                await ctx.send('That message ID is invalid.')
        else:
            await ctx.send('You\'re missing some arguments.')

    @commands.command()
    @commands.has_role('Developer')
    async def poll(self, ctx, *args):
        '''Make a poll message'''
        if ctx.message.channel_mentions:
            msg_text = ' '.join(args[1:]) + "\n\nReact with 👍 for **yes** or 👎 for **no**."
            msg = await ctx.message.channel_mentions[0].send(msg_text)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        else:
            await ctx.send('You need to specify a channel, sir.')

    #I'm not sure if this can be run if you're not the bot owner, so i've disabled it for now
    """@commands.command()
                async def shutdown(self, ctx):
                    '''Shuts down'''
                    await ctx.send('<:vive:683522338331033601> Shutting down.')
                    await ctx.bot.close()"""

def setup(bot):
    bot.add_cog(system(bot))
