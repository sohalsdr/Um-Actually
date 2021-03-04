import os
import language_tool_python
import discord
from dotenv import load_dotenv
from discord.ext import commands
from gingerit.gingerit import GingerIt

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

tool = language_tool_python.LanguageTool('en-US')

bot = commands.Bot(command_prefix='=')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='info', help='Displays information about the bot.')
async def info(ctx):
    info_embed = discord.Embed(
        title="Info",
        description=f'I\'m \"Um, Actually\", a bot to help check your grammar! I\'m not perfect, but I try my best! I\'m currently in **{len(bot.guilds)}** servers!', 
        color=discord.Color.blurple()
    )
    info_embed.set_footer(text='Made with <3 by ABlazingEBoy#7375')
    await ctx.send(embed=info_embed)


@bot.command(name='help', help='Shows this page.')
async def help(ctx, args=None):
    help_embed = discord.Embed(title="Command Usage", color=discord.Color.blurple())
    command_names_list = [x.name for x in bot.commands]

    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([str(i+1)+".  `"+x.name+"`" for i,x in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.set_footer(
            text="Type \'=help <command name>\' for more details about each command."
        )

    elif args in command_names_list:
        help_embed.add_field(
            name='`=' + args + '`',
            value=bot.get_command(args).help
        )

    else:
        help_embed.add_field(
            name="Umm ackchually,",
            value="that command doesn't exist."
        )

    await ctx.send(embed=help_embed)

@bot.command(name='ping', help='Basically useless, just tells you if the bot is running.')
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

@bot.command(name='check', help='Runs your text through Ginger and returns the result. Note: If you want to preserve formatting, wrap your entire text in quotation marks.')
async def ginger(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error", description="You didn't give me any text to parse!", color=discord.Color.red())
    else:
        text =  ' '.join(args)
        print('{} arguments: {}'.format(len(args), ' '.join(args)))

        parser = GingerIt()
        result = parser.parse(text)
        corrections = len(result['corrections'])

        print(result)

        embed=discord.Embed(title='Corrected Text', description=result['result'], color=discord.Color.blurple())
        embed.set_footer(text=f'{corrections} correction(s) made; Parser: Ginger; Requested by ' + ctx.author.name)
    await ctx.send(embed=embed)

@bot.command(name='check-langtool', help='Runs your text through LanguageTool and returns the result. This parser is slower, but sometimes yields better results. Note: If you want to preserve formatting, wrap your entire text in quotation marks.')
async def languagecheck(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error", description="You didn't give me any text to parse!", color=discord.Color.red())
    else:
        text = ' '.join(args)
        print('{} arguments: {}'.format(len(args), ' '.join(args)))
        
        matches = tool.check(text)
        result = tool.correct(text)

        embed=discord.Embed(title="Corrected Text", description=result, color=discord.Color.blurple())
        embed.set_footer(text=f'{len(matches)} correction(s) made; Parser: LanguageTool; Requested by ' + ctx.author.name)
    await ctx.send(embed=embed)

bot.run(TOKEN)