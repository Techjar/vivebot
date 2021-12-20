from discord.ext import commands
import discord


class Help(commands.Cog):
    """This"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    @commands.bot_has_permissions(embed_links=True)
    async def help_(self, ctx, *, item = None):
        """Help for cogs and commands."""

        async def can_run(command):
            try:
                return await command.can_run(ctx)
            except:
                return False

        if not item:
            embed = discord.Embed(
                title=f'{self.bot.user.name} Help Menu',
                description='\n'.join(f'{cog_name} - {(cog.description or "No description").splitlines()[0]}' for cog_name, cog in self.bot.cogs.items() if cog.get_commands()),
                color=0x82f4f4,
            )

        elif cog := self.bot.get_cog(item):
            embed = discord.Embed(
                title=f'Cog Help',
                description=(
                    '\n'.join([f'`{command.name}` - {(command.help or "No description").splitlines()[0]}' for command in cog.walk_commands() if not command.parent and (await can_run(command))])
                )[:4096],
                color=0x82f4f4,
            )

        elif command := self.bot.get_command(item):
            embed = discord.Embed(
                title=f'Command Help',
                description=f'>>> {command.help or "No help text available"}\n\n',
                color=0x82f4f4,
            )
            if isinstance(command, commands.Group):
                embed.description += '\n'.join([f'`{subcommand.name}` - {(subcommand.help or "No description").splitlines()[0]}' for subcommand in command.commands if len(subcommand.parents) == 1 and (await can_run(subcommand))])

            embed.description = embed.description[:4096]
            embed.add_field(name='Usage', value=f'`{ctx.prefix}{command.qualified_name} {command.signature}`')

        else:
            await ctx.send('That\'s not a cog or command.')
            return

        embed.set_footer(
            text=(
                f'Use {ctx.prefix}help <item> to find out more info on a cog or command.\n'
                'Ping shay#0038/Techjar#3305 if you have any issues with this bot.'
            )
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
