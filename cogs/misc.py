from discord.ext import commands
import time
import discord


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tester(self, ctx):
        """Assign or remove the tester role from yourself"""
        role = discord.utils.get(ctx.guild.roles, name='Tester')
        try:
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send(
                    f'Thanks, {ctx.author.mention}. You are no longer in the tester group.',
                    allowed_mentions=discord.AllowedMentions.none()
                )
            else:
                await ctx.author.add_roles(role)
                await ctx.send(
                    f'You are now in the tester group. Welcome aboard, {ctx.author.mention}.',
                    allowed_mentions=discord.AllowedMentions.none()
                )
        except discord.Forbidden:
            await ctx.send('I am unable to change your role, citizen.')


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
