from discord.ext import commands
import discord
import re
import random
import time
from datetime import date
import os
import asyncio
from aiohttp_requests import requests
import json
import traceback

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
spam_timer = {}

spam_domains = []
spam_domains_url = "https://api.hyperphish.com/gimme-domains"
spam_domains_last_update = 0

def is_birthday():
  today = date.today()
  return today >= date(today.year, 8, 4) and today < date(today.year, 8, 11)

async def update_status():
  while True:
    if is_birthday():
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Obama's Birthday Week"))
    else:
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Masses"))
    await asyncio.sleep(60)

async def update_spam_domains():
    global spam_domains
    global spam_domains_last_update
    if time.time() - spam_domains_last_update >= 1800:
        try:
            response = await requests.get(spam_domains_url, timeout=5)
            spam_domains = json.loads(await response.text())
            spam_domains_last_update = time.time()
        except:
            traceback.print_exc()

@bot.event
async def on_ready(): #we out here starting
    print(bot.user.name)
    print(bot.user.id)
    print("For the ViveCraft discord server\nCreated by shay#0038 (115238234778370049)")
    await update_spam_domains()
    await update_status()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == 628093260711198733 or message.content.startswith(prefix):
        return

    print('Message received from {0}#{1} ({2})'.format(message.author.name, message.author.discriminator, str(message.author.id)))

    obamasponce = ['You\'re welcome, citizen. <:obama:683186013392470031>', 'All in a day\'s work.', 'My pleasure.', 'No, thank you!'] #he kinda sounds like a cheesy superhero in these, idk how obama would respond to "thanks obama" so im clueless
    obamium = re.compile(r'(?i)(thanks obama|thanks, obama|thank you obama|thank you, obama)')
    if obamium.search(message.content):
        await message.channel.send(random.choice(obamasponce))
        print('They triggered obamium')

    if is_birthday():
      birthdaysponce = ['Thank you, citizen. 🥳', 'You\'re too kind.', 'It\'s no big deal.', 'Happy Birthday to you too. <:obamahead:727681381689196624>']
      birthdayium = re.compile(r'(?i)(happy birthday obama|happy birthday, obama)')
      if birthdayium.search(message.content):
          await message.channel.send(random.choice(birthdaysponce))
          print('They triggered birthdayium')

    if message.channel.id == 890473145801277441:
        try:
            with open(os.environ.get('DATA_DIR') + 'serveradrulesmsgid.txt', 'r') as file:
                msg_id = int(file.read())
            old_message = await message.channel.fetch_message(msg_id)
            await old_message.delete()
        except:
            pass
        
        new_message = await message.channel.send("If you're posting a server ad, be sure to read the rules in this channel's pins! 📌\nThe important parts are highlighted in bold.")
        with open(os.environ.get('DATA_DIR') + 'serveradrulesmsgid.txt', 'w') as file:
            file.write(str(new_message.id))

    global update_cooldown
    with open(os.environ.get('DATA_DIR') + 'updateversion.txt', 'r') as file:
        fifteenium_version = file.read()
    fifteenium = re.compile('(?i)({0}.*when|when.*{0}|{0}.*update|update.*{0}|updated.*{0}|vivecraft.*{0}|{0}.*vivecraft|port.*{0}|{0}.*port|{0}.*available|available.*{0}|{0}.*progress|progress.*{0}|{0}.*develop|develop.*{0}|{0}.*release|release.*{0})'.format(fifteenium_version.replace('.', '\.')))
    if message.channel.id != int(os.environ.get('UPDATE_CHANNEL_ID')) and message.channel.id != 890473145801277441 and fifteenium_version != "null" and len(message.content.split()) >= 5 and fifteenium.search(message.content) and (time.time() - update_cooldown) > 300:
        with open(os.environ.get('DATA_DIR') + 'updateprogress.txt', 'r') as file:
            progress = file.read()
        update_cooldown = time.time()
        update_channel = discord.utils.get(message.guild.channels, id = int(os.environ.get('UPDATE_CHANNEL_ID')))
        await message.reply('Vivecraft will be updated to Minecraft {0} as soon as possible, citizen.\nThe current progress is: {1}\nI\'m a busy man, so you can read the most up-to-date progress at any time in {2}.'.format(fifteenium_version, progress, update_channel.mention))
        print('They triggered the progress query')

    await update_spam_domains()

    dev_role = discord.utils.find(lambda r: r.name == 'Developer', message.guild.roles)
    if not dev_role in message.author.roles:
        matched = False
        matched_words = ""
        with open(os.environ.get('DATA_DIR') + 'filters.txt', 'r') as file:
            for line in file.read().splitlines():
                words = line.split()
                if words:
                    matched = all(re.search(flt, message.content, re.IGNORECASE) for flt in words)
                    if matched:
                        matched_words = line
                        break
        if not matched:
            for domain in spam_domains:
                matched = re.search(domain, message.content, re.IGNORECASE)
                if matched:
                    matched_words = domain
                    break
        if matched:
            print('Spam detected! Matcher was: ' + matched_words)
            if message.author.id in spam_timer:
                timer = spam_timer[message.author.id]
                if time.time() - timer['time'] < 30:
                    timer['count'] += 1
                else:
                    timer['count'] = 1
                if timer['count'] >= 2:
                    jail_channel = discord.utils.get(message.guild.channels, id = int(os.environ.get('JAIL_CHANNEL_ID')))
                    muted_role = discord.utils.get(message.guild.roles, name="Muted")
                    if muted_role not in message.author.roles:
                        await message.author.add_roles(muted_role)
                        await jail_channel.send('{0} was muted for sending spam. Matched words: `{1}`'.format(message.author.mention, matched_words))
                        try:
                            await message.author.send('You were muted for sending spam. This is likely due to your account being compromised. Once you\'ve recovered your account, or if this in error, please message one of the developers/admins to be unmuted.')
                        except:
                            pass
                        print('Muted them for sending too much spam!')
                timer['time'] = time.time()
            else:
                spam_timer[message.author.id] = {'count': 1, 'time': time.time()}
            await message.delete()
                        
                

# Regex thing, Techjar said to remove it so i did. here it is just in case you want to re-enable
#@bot.event
#async def on_message(message): #aah oh no i cant read
#    await bot.process_commands(message)
#    hmd = re.compile(r'(?i)((on )(headset|hmd|oculus|rift|vive))|((showing |displaying )(on|on the|on our)( monitor| monnitor| screen| steamvr))|(hmd|headset|oculus|rift|vive)( doesnt| doesn\'t| don\'t| dont| wont| won\'t)')
#    match = hmd.search(message.content)
#    if match and message.author.id != 598277022787043370 and '?bp' not in message.content.lower():
#        await message.channel.send("{}, it sounds like the game is displaying on your monitor, but not the headset. If this is the case, may I remind you to read the FAQ before posting such inquiries. It's the first thing there!\n<http://www.vivecraft.org/faq/#troubleshooting>".format(message.author.mention))

if os.path.exists('token.txt'):
    with open('token.txt') as f:
        token = f.readline()
else:
    token = os.environ.get('BOT_TOKEN')

bot.run(token)
