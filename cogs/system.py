from discord.ext import commands
import discord
import time


class System(commands.Cog):
    """General-purpose commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Show the bot\'s latency"""
        ping_prior = time.monotonic()
        message = await ctx.send('*:ping_pong:*')
        ping = round((time.monotonic() - ping_prior) * 1000, 2)
        await message.edit(content=f'{int(ping)}ms')

    @commands.command()
    async def info(self, ctx):
        """Show info about the bot"""
        embed = discord.Embed(
            title=f'{self.bot.user.name} Info',
            description=(
                f'This bot was created on {discord.utils.format_dt(self.bot.user.created_at)} for the Vivecraft Discord server. '
                'You can find its source on [GitHub](https://github.com/Techjar/vivebot). <:obama:683186013392470031>'
            ),
            color=0x82f4f4,
        )
        embed.add_field(name='Library', value=f'[discord.py {discord.__version__}](https://github.com/Rapptz/discord.py)')
        embed.set_footer(text='Ping shay#0038/Techjar#3305 if you have any issues with this bot.')
        await ctx.send(embed=embed)

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
