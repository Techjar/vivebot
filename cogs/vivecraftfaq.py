import aiohttp
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from discord.ext import commands
import discord
import re


class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def find_faq_entry(self, query):
        response = await self.bot.session.get("http://www.vivecraft.org/faq/", timeout=5)
        resp_text = await response.text()

        def wrapped():
            soup = BeautifulSoup(resp_text, 'html.parser')
            root = soup.find('div', class_='entry-content')

            found_data = {
                'title': '',
                'id': '',
                'description': '',
                'image_url': None,
            }

            found = False
            for mode in range(0, 2):
                if found:
                    break
                for element in root.find_all('div', recursive=False):
                    title_element = element.find('blockquote')
                    if (
                        title_element is not None
                        and (
                            (mode == 0 and element.attrs['id'] == query.split()[0].lower())
                            or (mode == 1 and query.lower() in title_element.find('p').text.lower())
                        )
                    ):
                        found_data['id'] = element.attrs['id']
                        found_data['title'] = title_element.find('p').text
                        for part in element.find_all(True, recursive=False):
                            if part.name == 'p':
                                if found_data['image_url'] is None:
                                    if part.find_all('img'):
                                        found_data['image_url'] = part.find_all('img')[0].attrs['src']

                                if not part.text.strip():
                                    continue
                                for tag in part.contents:
                                    if isinstance(tag, NavigableString):
                                        found_data['description'] += tag
                                    elif tag.name == 'a':
                                        link = tag.attrs['href']
                                        if not re.match(r'^[a-z0-9]+://', link, re.IGNORECASE):
                                            if link.startswith('/'):
                                                link = f'http://www.vivecraft.org{link}'
                                            else:
                                                link = f'http://www.vivecraft.org/faq/{link}'
                                        found_data['description'] += f'[{tag.text}]({link})'
                                    elif tag.name == 'strong':
                                        found_data['description'] += f'**{tag.text}**'
                                    elif tag.name == 'i':
                                        found_data['description'] += f'*{tag.text}*'
                                    else:
                                        found_data['description'] += tag.text
                                found_data['description'] += '\n\n'

                            elif part.name == 'ul':
                                for item in part.find_all('li'):
                                    found_data['description'] += f'• {item.text.strip()}\n'
                                found_data['description'] += '\n'

                            elif part.name == 'ol':
                                for i, item in enumerate(part.find_all('li'), start=1):
                                    found_data['description'] += f'{i}. {item.text.strip()}\n'
                                found_data['description'] += '\n'

                        found = True
                        break

            return found_data

        result = await self.bot.loop.run_in_executor(None, wrapped)
        return result

    async def find_download_links(self):
        response = await self.bot.session.get('http://www.vivecraft.org/downloads/', timeout=5)
        resp_text = await response.text()

        def wrapped():
            soup = BeautifulSoup(resp_text, 'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')

            found_data = {
                'versions': []
            }

            for cell in rows[0].find_all('th')[1:]:
                found_data['versions'].append({'name': cell.text})

            def find_urls(row, key):
                span_acc = 0
                for idx, cell in enumerate(rows[row].find_all('td')[1:]):
                    link = cell.find('a')
                    if link is not None:
                        span = int(cell.attrs['colspan']) if 'colspan' in cell.attrs else 1
                        for i in range(0, span):
                            found_data['versions'][idx + span_acc + i][key] = link.attrs['href']
                        span_acc += span - 1

            find_urls(2, 'client_url')
            find_urls(4, 'spigot_url')
            find_urls(5, 'forge_url')

            return found_data

        result = await self.bot.loop.run_in_executor(None, wrapped)
        return result

    @commands.command(aliases=['questions', 'issue', 'issues'])
    async def faq(self, ctx, *, query = None):
        """Display jumpable buttons to the FAQ or a specific entry from the FAQ"""
        if not query:
            embed = discord.Embed(color=0x82f4f4)
            embed.set_author(name='FAQ - Jump To:', icon_url='https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png')
            embed.add_field(name='Gameplay', value='http://www.vivecraft.org/faq/#gameplay', inline=True)
            embed.add_field(name='Compatibility', value='http://www.vivecraft.org/faq/#compatibility', inline=True)
            embed.add_field(name='Troubleshooting', value='http://www.vivecraft.org/faq/#troubleshooting', inline=True)
            embed.set_footer(text='Ping shay#0038/Techjar#3305 if you have any issues with this bot.')
            await ctx.send(embed=embed)
            return

        async with ctx.typing():
            found = await self.find_faq_entry(query)
            if not found['id']:
                await ctx.send('Nothing found.')
                return

            embed = discord.Embed(
                description=found['description'],
                color=0x82f4f4
            )
            embed.set_author(
                name=f'FAQ - {found["title"]}',
                url=f'http://www.vivecraft.org/faq/#{found["id"]}',
                icon_url='https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png',
            )
            embed.add_field(
                name='For more questions see the full FAQ',
                value='http://www.vivecraft.org/faq/',
                inline=True
            )
            if found['image_url']:
                embed.set_image(url=found['image_url'])

            await ctx.send(embed=embed, reference=ctx.message.reference)
            if ctx.message.reference:
                await ctx.message.delete()

    @commands.command(aliases=['download', 'dl'])
    async def downloads(self, ctx):
        """Show Vivecraft download links"""
        found = await self.find_download_links()
        embed = discord.Embed(
            description='Installation instructions can be found at [vivecraft.org/downloads](http://www.vivecraft.org/downloads/). All download links can also be found there, including discontinued legacy versions.',
            color=0x5e9d34
        )
        embed.set_author(
            name='Downloads',
            url='http://www.vivecraft.org/downloads/',
            icon_url='https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png',
        )
        for version in found['versions']:
            field_desc = f'[VR & Non-VR Client]({version["client_url"]})'
            if 'spigot_url' in version:
                field_desc += f'\n[Spigot Server Plugin]({version["spigot_url"]})'
            if 'forge_url' in version:
                field_desc += f'\n[Forge Server Mod]({version["forge_url"]})'
            embed.add_field(name=version['name'], value=field_desc)

        await ctx.send(embed=embed, reference=ctx.message.reference)
        if ctx.message.reference is not None:
            await ctx.message.delete()

    @commands.command()
    async def forum(self, ctx):
        """Link to the forum"""
        embed = discord.Embed(color=0x82f4f4)
        embed.set_author(name='Forum - Jump To:', icon_url='https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png')
        embed.add_field(name='Main Page', value='http://www.vivecraft.org/forum/')
        embed.add_field(name='General', value='http://www.vivecraft.org/forum/viewforum.php?f=6')
        embed.add_field(name='Troubleshooting', value='http://www.vivecraft.org/forum/viewforum.php?f=3')
        embed.add_field(name='Multiplayer', value='http://www.vivecraft.org/forum/viewforum.php?f=4')
        embed.add_field(name='Modpacks', value='http://www.vivecraft.org/forum/viewforum.php?f=7')
        embed.set_footer(text='Ping shay#0038/Techjar#3305 if you have any issues with this bot.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FAQ(bot))
