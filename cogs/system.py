from discord.ext import commands
import discord
import time


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Show the bot\'s latency"""
        pingprior = time.monotonic()
        ping = discord.Embed(title='Pong! :ping_pong:', description='```xl\n<:vive:683522338331033601> Waiting to finish...```')
        message=await ctx.send(embed=ping)
        ping=(time.monotonic() - pingprior) * 1000
        pong = discord.Embed(title='Pong! :ping_pong:', description=f'```xl\n{int(ping)}ms    ```')
        await message.edit(embed=pong)#content=f"Pong!  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

    @commands.command()
    async def info(self, ctx):
        """Show info about the bot"""
        infbed = discord.Embed(title='🖥 Info', description=' ', color=0x96c6fa)
        infbed.add_field(name='📚 Library', value='`Discord.py`', inline=True)
        infbed.add_field(name='<:vive:683522338331033601> Version', value='`v0.1`', inline=True)
        infbed.set_footer(text='Created by shay#0038 (115238234778370049)')
        await ctx.send(embed=infbed)

    @commands.command()
    @commands.has_role('Developer')
    async def say(self, ctx, channel: discord.TextChannel, *, content):
        """Make the bot say something"""
        await channel.send(content[:2000])

    @commands.command()
    @commands.has_role('Developer')
    async def react(self, ctx, message: discord.Message, emoji: discord.PartialEmoji):
        """Make the bot react to a message"""
        await message.add_reaction(emoji)

    @commands.command()
    @commands.has_role('Developer')
    async def poll(self, ctx, channel: discord.TextChannel, *, content):
        """Create a poll message"""
        msg_text = '\n\nReact with \N{THUMBS UP SIGN} for **yes** or \N{THUMBS DOWN SIGN} for **no**.'
        msg_text = content[:len(msg_text)] + msg_text
        msg = await channel.send(msg_text)
        await msg.add_reaction('\N{THUMBS UP SIGN}')
        await msg.add_reaction('\N{THUMBS DOWN SIGN}')


def setup(bot):
    bot.add_cog(System(bot))
