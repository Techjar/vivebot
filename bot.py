from discord.ext import commands
import discord
import re
import random
import time

prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help') #removes ?help for the custom one cause i dont like discord.py's default ?help
#these cogs really just exist so that i dont have to cram it all in the main file.
bot.load_extension("cogs.help") #take a guess
bot.load_extension("cogs.vivecraftfaq")
bot.load_extension("cogs.system")
bot.load_extension("cogs.updateprogress")
bot.load_extension("cogs.misc")

update_cooldown = 0

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

    print('Message received from {0}#{1} ({2})'.format(message.author.name, message.author.discriminator, str(message.author.id)))

    obamasponce = ['You\'re welcome, citizen. <:obama:683186013392470031>', 'All in a day\'s work.', 'My pleasure.', 'No, thank you!'] #he kinda sounds like a cheesy superhero in these, idk how obama would respond to "thanks obama" so im clueless
    obamium = re.compile(r'(?i)(thanks obama|thanks, obama|thank you obama|thank you, obama)')
    if obamium.search(message.content):
        await message.channel.send(random.choice(obamasponce))
        print('They triggered obamium')

    global update_cooldown
    with open('updateversion.txt', 'r') as file:
        fifteenium_version = file.read()
    fifteenium = re.compile('(?i)({0}.*when|when.*{0}|{0}.*update|update.*{0}|updated.*{0}|vivecraft.*{0}|{0}.*vivecraft|port.*{0}|{0}.*port|{0}.*available|available.*{0}|{0}.*progress|progress.*{0}|{0}.*develop|develop.*{0}|{0}.*release|release.*{0})'.format(fifteenium_version.replace('.', '\.')))
    if fifteenium.search(message.content) and (time.time() - update_cooldown) > 300:
        with open('updateprogress.txt', 'r') as file:
            progress = file.read()
        update_cooldown = time.time()
        await message.channel.send('Vivecraft will be updated to MC {0} as soon as possible.\nCurrent progress: {1}'.format(fifteenium_version, progress))

    dev_role = discord.utils.find(lambda r: r.name == 'Developer', message.guild.roles)
    if not dev_role in message.author.roles:
        with open('filters.txt', 'r') as file:
            for line in file.read().splitlines():
                matched = all(re.search(flt, message.content, re.IGNORECASE) for flt in line.split(' '))
                if matched:
                    await message.delete()
                    print('Deleted their spam! Matcher was: ' + line)
                

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
