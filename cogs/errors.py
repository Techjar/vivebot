import discord
from discord.ext import commands
import sys


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send(str(error), allowed_mentions=discord.AllowedMentions.none())

        elif isinstance(error, commands.BotMissingPermissions):
            missing = '**, **'.join(error.missing_permissions)
            await ctx.send(f'I am missing the following permissions: **{missing}**')

        elif isinstance(error, commands.MissingPermissions):
            missing = '**, **'.join(error.missing_permissions)
            await ctx.send(f'You are missing the following permissions: **{missing}**')

        elif isinstance(error, commands.MissingRole):
            await ctx.send(f'You need the following role: **{error.missing_role}**')

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'You need one of the following roles: **{"**, **".join(error.missing_roles)}**')

        elif isinstance(error, commands.CheckFailure):
            await ctx.send('One of the checks for this command failed. This usually means you are not allowed to run it.')

        else:
            print(f'Exception in command {ctx.command.name}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            embed = discord.Embed(
                title='An error occurred',
                description='Please report this to @Techjar#3305',
                color=0xff0000
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
