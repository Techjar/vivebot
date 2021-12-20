import aiohttp
import asyncio
from datetime import date
from discord.ext import commands
import discord
import os
import re
import random
import time

prefix = '?'
bot = commands.Bot(
    command_prefix=prefix,
    activity=discord.Activity(type=discord.ActivityType.watching, name='The Masses'),
    help_command=None,
)

bot.load_extension('cogs.help')
bot.load_extension('cogs.vivecraftfaq')
bot.load_extension('cogs.system')
bot.load_extension('cogs.updateprogress')
bot.load_extension('cogs.misc')
bot.load_extension('cogs.errors')

update_cooldown = 0
spam_timer = {}

def is_birthday():
    today = date.today()
    return today >= date(today.year, 8, 4) and today < date(today.year, 8, 11)

async def update_status():
    birthday_activity = discord.Activity(type=discord.ActivityType.playing, name='Obama\'s Birthday Week')
    normal_activity = discord.Activity(type=discord.ActivityType.watching, name='The Masses')
    while True:
        current_activity = bot.guilds[0].me.activity or bot.activity
        if is_birthday() and current_activity.name != birthday_activity.name:
            await bot.change_presence(activity=birthday_activity)
        elif current_activity.name != normal_activity.name:
            await bot.change_presence(activity=normal_activity)
        await asyncio.sleep(3600)

@bot.event
async def on_ready():
    print(
        f'{bot.user} ({bot.user.id})\n'
        'Created for the Vivecraft Discord server by shay#0038 (115238234778370049)'
    )

async def init():
    await bot.wait_until_ready()
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    await update_status()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == 628093260711198733 or message.content.startswith(prefix):
        return

    print(f'Message received from {message.author} ({message.author.id})')

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

    dev_role = discord.utils.find(lambda r: r.name == 'Developer', message.guild.roles)
    if not dev_role in message.author.roles:
        with open(os.environ.get('DATA_DIR') + 'filters.txt', 'r') as file:
            for line in file.read().splitlines():
                words = line.split()
                if words:
                    matched = all(re.search(flt, message.content, re.IGNORECASE) for flt in words)
                    if matched:
                        print('Spam detected! Matcher was: ' + line)
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
                                    await jail_channel.send('{0} was muted for sending spam. Matched words: `{1}`'.format(message.author.mention, line))
                                    await message.author.send('You were muted for sending spam. This is likely due to your account being compromised. Once you\'ve recovered your account, message one of the developers/admins to be unmuted.')
                                    print('Muted them for sending too much spam!')
                            timer['time'] = time.time()
                        else:
                            spam_timer[message.author.id] = {'count': 1, 'time': time.time()}
                        await message.delete()
                        break

if os.path.exists('token.txt'):
    with open('token.txt') as f:
        token = f.readline()
else:
    token = os.environ.get('BOT_TOKEN')

bot.loop.create_task(init())
bot.run(token)
