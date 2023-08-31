from discord.ext import commands
import time
import discord
import os

class updateprogress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_message(self, ctx):
        with open(os.environ.get('DATA_DIR') + 'updateversion.txt', 'r') as file:
            fifteenium_version = file.read()
        with open(os.environ.get('DATA_DIR') + 'updateprogress.txt', 'r') as file:
            progress = file.read()
        message_str = 'Vivecraft will be updated to Minecraft {0} as soon as possible, citizens.\nThe current progress is: {1}'.format(fifteenium_version, progress)
        
        channel = discord.utils.get(ctx.guild.channels, id = int(os.environ.get('UPDATE_CHANNEL_ID')))
        try:
            with open(os.environ.get('DATA_DIR') + 'updatemsgid.txt', 'r') as file:
                msg_id = int(file.read())
            message = await channel.fetch_message(msg_id)
            await message.delete()
        except:
            print("Update message not found")
        
        if fifteenium_version != "null":
            new_message = await channel.send(message_str)
            await new_message.publish()
            with open(os.environ.get('DATA_DIR') + 'updatemsgid.txt', 'w') as file:
                file.write(str(new_message.id))
        
        await ctx.send('**Update query will respond to {0}, and response is now:**\n{1}'.format(fifteenium_version, message_str))

    @commands.command()
    @commands.has_role('Developer')
    async def progress(self, ctx, *, arg):
        '''Sets update progress'''
        if len(arg) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open(os.environ.get('DATA_DIR') + 'updateprogress.txt', 'w') as file:
            file.write(arg)
        await self.update_message(ctx)

    @commands.command()
    @commands.has_role('Developer')
    async def update(self, ctx, *, arg):
        '''Sets update version'''
        if len(arg) == 0:
            await ctx.send('You need to provide more arguments, sir.')
            return
        with open(os.environ.get('DATA_DIR') + 'updateversion.txt', 'w') as file:
            file.write(arg)
        await self.update_message(ctx)

async def setup(bot):
    bot.add_cog(updateprogress(bot))
