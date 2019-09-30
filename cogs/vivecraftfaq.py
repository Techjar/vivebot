from discord.ext import commands
import discord

class faq(commands.Cog, name='FAQ'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['questions'])
    async def faq(self, ctx):
        '''Displays jumpable buttons to the FAQ'''
        embed = discord.Embed(title=" ", color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Jump To:", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        embed.add_field(name="Gameplay", value="http://www.vivecraft.org/faq/#gameplay", inline=True)
        embed.add_field(name="Compatibility", value="http://www.vivecraft.org/faq/#compatibility", inline=True)
        embed.add_field(name="Troubleshooting", value="http://www.vivecraft.org/faq/#troubleshooting", inline=True)
        embed.set_footer(text="ping @shay#0038 if you have any issues!")
        await ctx.send(embed=embed)

    @commands.group(aliases=['issues'])
    async def issue(self, ctx):
        '''Issues from the F.A.Q.'''

    @issue.command(aliases=['list', 'display'])
    async def show(self, ctx):
        '''list all'''
        embed = discord.Embed(title="Syntax: ?issue <subcommand>", description="**hmd** - Monitor, not HMD\n"
                              "**run** - Game runs poorly\n"
                              "**click** - Can't click on anything\n"
                              "**blurry** - Shaderpack makes stuff blurry\n"
                              "**controllers** - Motion controls don't work\n"
                              "**optifine** - Installer failed to download opti\n"
                              "**blackscreen** - Starts with a black screen\n"
                              "**crash** - Crashes on startup\n"
                              "**logs** - Shows where to finds logs\n"
                              "**jar** - Crashes and complains about a modified jar\n"
                              "**mcf** - Crashes and says something about a malformed class name\n"
                              "**heapsize** - Crashes and says info error occurred during VM initialization\n"
                              "**reservespace** - Crashes and says it could not reserve space for the object heap\n"
                              "**javabinary** - Crashes and says the Java Binary SE stopped working\n"
                              "**exceptionaccess** - Crashes and says EXCEPTION_ACCESS_VIOLATION in d3d9.dll",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting List", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['monitor', 'common', 'stopasking'])
    async def hmd(self, ctx):
        '''Showing on monitor, not hmd, yadda yadda'''
        embed = discord.Embed(title="The game shows up on my desktop, but not in the headset!",
                              description="This occurs frequently on systems with dual GPUs like Alienware laptops. The solution is to force your PC to always use the gaming GPU. For NVIDIA systems right click the desktop and open the NVIDIA Control Panel. Set the Graphics Processor option to ‘High Performance’. If that isn’t the issue, ensure your monitor and HMD are plugged into the dedicated GPU. If that isn’t the issue, makes sure you didn’t install the Non-VR version by mistake.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/HMD", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        embed.set_image(url="https://i2.wp.com/www.vivecraft.org/wp-content/uploads/2016/07/unknown.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['performance', 'poorly'])
    async def run(self, ctx):
        '''Runs poorly'''
        embed = discord.Embed(title="The game runs poorly, what can I do?",
                              description="Minecraft was not written for VR and is not a very well optimized game. Here are some steps you can take to improve performance.\n\n"
                              "• Make sure you are allocating enough RAM for your installation type. Additionally be aware it’s possible to have your Java heap space overridden by Windows environment variables. If the game run incredibly bad check for a unwanted - Xmx256M argument there.\n"
                              "• Reduce your draw distance in the Video Settings menu. Below 10 is best, even for high-end systems.\n"
                              "• Turn down the ‘Render Scale’ in the VR Settings > Stereo Rendering menu. Also make sure your SteamVR supersampling is at 1.0, Vivecraft has its own setting and will stack with SteamVR’s.\n"
                              "• Make sure you are not using any custom shaders or texture packs (in Video Settings).",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Performance Issue", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command()
    async def click(self, ctx):
        '''cant click on anything'''
        embed = discord.Embed(title="I can't click on anything!",
                              description="Make sure the desktop window is not minimized. Alt-tabbing from a fullscreen game will minimize it. If you need to play without the game window in focus be sure to set it to windowed mode via the video settings or F11.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Click", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['blurry', 'shaderpack'])
    async def shader(self, ctx):
        '''blurry boyy'''
        embed = discord.Embed(title="I’m using a shader pack and everything is blurry!",
                              description="Check the specific settings for your shader and disable motion blur, depth-of-field, lens flare, or similar.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Shaderpack", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['motioncontrols'])
    async def controllers(self, ctx):
        '''aaa oh no'''
        embed = discord.Embed(title="The motion controllers don’t respond at all!",
                              description="Make sure the game is set to STANDING play mode. Use the mouse to navigate the menu to the VR Settings screen and change it there.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Motion Controllers", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['protocolfamily', 'optifineinstall', 'failed', 'opti'])
    async def optifine(self, ctx):
        '''opti'''
        embed = discord.Embed(title="The Vivecraft installer says ‘Failed to download Optifine: Address family not supported by protocol family: connect’",
                              description="See [this page](https://stackoverflow.com/questions/16373906/address-family-not-supported-by-protocol-family-socketexception-on-a-specific) for some potential solutions",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Optifine", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['steamerror', 'errormsg'])
    async def blackscreen(self, ctx):
        '''starts'''
        embed = discord.Embed(title="The game starts on a black screen with a SteamVR error message",
                              description="Error 108: No HMD Found. Ensure you have SteamVR Installed and your HMD is working.\n"
                              "Error 112: Log path not found. This happens when your steam installation has moved. In SteamVR Settings > Developer Options click the Log Path button and set it whereever your steamapp/common/SteamVR directory is.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Starts Black", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['startup', 'crashes'])
    async def crash(self, ctx):
        '''startup'''
        embed = discord.Embed(title="The game crashes on startup, what should I do?",
                              description="You will need more information about the crash. Depending on the type of crash this information may be in different log files. Once you have found the correct error message, Keep reading for solutions to common ones.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash on Startup", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command()
    async def logs(self, ctx):
        '''where findo'''
        embed = discord.Embed(title="Where do I find Minecraft logs?",
                              description="• First check your %appdata%.minecraft\\crash-reports\\ directory and look for a newly created file. This file will contain the crash information if the game crashed while it was running. In the case of mod conflict crashes you may also need to look at the latest.log file.\n"
                              "• Next check the .minecraft/logs / directory and look for ‘latest.log’. (If you are using Forge on 1.10 look for ‘fml-client-latest.log’). The last entry in this file should be the crash stacktrace. This file also contains the startup sequence and is usually better for troubleshooting, but may be confusing if you don’t know how to read it. Like the crash reports, latest.log is only created if the game properly initializes.\n"
                              "• In some cases, no latest.log file is created or no error is logged. This frequently occurs if Java fails to initialize due to RAM allocation issues. In these cases check the root .minecraft folder for a file called launcher_log.txt. The crash should be at or near the bottom of this file.\n"
                              "• In rare cases the Java Virtual Machine itself may crash due to memory or driver issues. In these cases a file called hs_err_pidXXX.log will be created in the root .minecraft directory.\n\n"
                              "If your crash is not listed below or you are unsure how to read the logs, come to the Discord or Forum and bring your log. *(hey look, you're already in the discord! hello!)*",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Logs", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['modified', 'moddedjar', 'willnowexit'])
    async def jar(self, ctx):
        embed = discord.Embed(title="The game crashes and the error says “The game will now exit” and complains about a modified jar",
                              description="Your profile is launching Forge and is missing some critical JVM arguments. The Vivecraft installer adds these to the profile, but may have been deleted. Ensure your profile JVM args includes `-Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true`",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash + Modified Jar", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['malformed', 'classname', 'mfc'])
    async def malformedclassname(self, ctx):
        embed = discord.Embed(title="The game crashes and the error says \"MalformedClassName\"",
                              description="Go to your .minecraft directory and delete usercache.json. That should sort it.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash + Malformed Class Name", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['crashheap', 'vmheap', 'maximumheap', 'javaheapspace'])
    async def heapsize(self, ctx):
        embed = discord.Embed(title="The game crashes and the error says \"Info Error occurred during initialization of VM Initial heap size set to a larger value than the maximum heap size Picked up _JAVA_OPTIONS: -Xmx###M: Java heap space\"",
                              description="Check your Windows environment variables for an entry called _JAVA_OPTS that is adding a Xmx256M or similar argument to your java commands. Remove it.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash During VM Initialization", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['couldnotreserve', 'couldntreserve', '2097152', 'objectheap'])
    async def reservespace(self, ctx):
        embed = discord.Embed(title="The game crashes and the error says \"Could not reserve enough space for 2097152KB object heap\"",
                              description="You do not have 64-bit java installed. Install it or allocate less RAM to the Vivecraft profile. 64-bit and **at least** 2GB RAM is recommended for VR.\n"
                              "Go get [__Windows Offline (64-bit)__ from here](https://www.java.com/en/download/manual.jsp).",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash + Could not Reserve Space", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @issue.command(aliases=['binaryse', 'javabinaryse', 'javase', 'jbse', 'jbs'])
    async def javabinary(self, ctx):
        embed = discord.Embed(title="The game crashes and the popup window says 'Java Binary SE has stopped working'",
                              description="This is caused by a buggy nvidia driver released in January 2017 (v378.49). Try updating your drivers.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash + Could not Reserve Space", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)
    
    @issue.command(aliases=['accessviolation', 'exceptionaccessviolation', 'eav', 'd3d9.dll'])
    async def exceptionaccess(self, ctx):
        embed = discord.Embed(title="The game (or the installer) crashes and says 'EXCEPTION_ACCESS_VIOLATION' in 'd3d9.dll'",
                              description="This is caused by an incompatibility between Windows 10 creators update, 64-bit java, and Rivatuner. You will need to either uninstall or update Rivatuner.",
                              color=0x82f4f4)
        embed.set_author(name="F.A.Q. - Troubleshooting/Crash + Could not Reserve Space", url="http://www.vivecraft.org/faq/#troubleshooting",
                         icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def forum(self, ctx):
        '''Link to the forum'''
        embed = discord.Embed(title=" ", color=0x82f4f4)
        embed.set_author(name="Forum - Jump To:", icon_url="https://media.discordapp.net/attachments/548280483809722369/621835686030475274/vc.png")
        embed.add_field(name="Main Page", value="http://www.vivecraft.org/forum/", inline=True)
        embed.add_field(name="General", value="http://www.vivecraft.org/forum/viewforum.php?f=6&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Troubleshooting", value="http://www.vivecraft.org/forum/viewforum.php?f=3&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Multiplayer", value="http://www.vivecraft.org/forum/viewforum.php?f=4&sid=d4cc7691f24945f5a4b7c49c210684fd", inline=True)
        embed.add_field(name="Modpacks", value="http://www.vivecraft.org/forum/viewforum.php?f=7&sid=86d1ec6bd700699b3484b5083bbb6da4", inline=True)
        embed.set_footer(text="ping @shay if you have any issues!")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(faq(bot))
