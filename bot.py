from discord.ext import commands
import discord
#import re #this is for the response thing, uncomment this if you want to enable it
prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help') #removes ?help for the custom one cause i dont like discord.py's default ?help
#these cogs really just exist so that i dont have to cram it all in the main file.
bot.load_extension("cogs.help") #take a guess
bot.load_extension("cogs.vivecraftfaq")
bot.load_extension("cogs.system")

@bot.event
async def on_ready(): #we out here starting
    print(bot.user.name)
    print(bot.user.id)
    print("For the ViveCraft discord server\nCreated by shay#0038 (115238234778370049)")

# Regex thing, Techjar said to remove it so i did. here it is just in case you want to re-enable
#@bot.event
#async def on_message(message): #aah oh no i cant read
#    await bot.process_commands(message)
#    hmd = re.compile(r'(?i)((on )(headset|hmd|oculus|rift|vive))|((showing |displaying )(on|on the|on our)( monitor| monnitor| screen| steamvr))|(hmd|headset|oculus|rift|vive)( doesnt| doesn\'t| don\'t| dont| wont| won\'t)')
#    match = hmd.search(message.content)
#    if match and message.author.id != 598277022787043370 and '?bp' not in message.content.lower():
#        await message.channel.send("{}, it sounds like the game is displaying on your monitor, but not the headset. If this is the case, may I remind you to read the FAQ before posting such inquiries. It's the first thing there!\n<http://www.vivecraft.org/faq/#troubleshooting>".format(message.author.mention))

with open('token.txt') as f:
    token = f.readline()

bot.run(token)
