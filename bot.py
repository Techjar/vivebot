from discord.ext import commands
import discord
import re
import random
prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help') #removes ?help for the custom one cause i dont like discord.py's default ?help
#these cogs really just exist so that i dont have to cram it all in the main file.
bot.load_extension("cogs.help") #take a guess
bot.load_extension("cogs.vivecraftfaq")
bot.load_extension("cogs.system")
bot.load_extension("cogs.updateprogress")

@bot.event
async def on_ready(): #we out here starting
    print(bot.user.name)
    print(bot.user.id)
    print("For the ViveCraft discord server\nCreated by shay#0038 (115238234778370049)")

@bot.event
async def on_message(message): #budda asked for it, feel free to remove or comment out
    await bot.process_commands(message)
    if message.author.id == 628093260711198733:
        return

    obamasponce = ['You\'re welcome, citizen.', 'All in a day\'s work.', 'My pleasure.', 'No, thank you!'] #he kinda sounds like a cheesy superhero in these, idk how obama would respond to "thanks obama" so im clueless
    obamium = re.compile(r'(?i)(thanks obama|thanks, obama|thank you obama|thank you, obama)')
    if obamium.search(message.content):
        await message.channel.send(random.choice(obamasponce))

    fifteenium = re.compile(r'(?i)(1.15\.*when|when.*1\.15|1\.15.*update|update.*1\.15|updated.*1\.15|vivecraft.*1\.15|1\.15.*vivecraft|port.*1\.15|1\.15.*port|1\.15.*available|available.*1\.15)')
    if fifteenium.search(message.content):
        with open('115progress.txt', 'r') as file:
            progress = file.read()
        await message.channel.send('Vivecraft will be updated to MC 1.15 as soon as possible.\nCurrent progress: ' + progress)

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
