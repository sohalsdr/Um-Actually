import os
import language_tool_python
from dotenv import load_dotenv
from discord.ext import commands
from gingerit.gingerit import GingerIt

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

tool = language_tool_python.LanguageTool('en-US')

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping', help='Basically useless, just tells you if the bot is running.')
async def pong(ctx):
    await ctx.send('pong!')

@bot.command(name='check-ginger', help='Runs your text through Ginger and returns the result')
async def ginger(ctx, *args):
    if not args:
        await ctx.send('You didn\'t give me any text to parse!')
    else:
        text =  ' '.join(args)
        print('{} arguments: {}'.format(len(args), ' '.join(args)))

        parser = GingerIt()
        result = parser.parse(text)
        corrections = len(result['corrections'])

        print(result)

        await ctx.send('**Corrected text:** ')
        await ctx.send(result['result'])
        await ctx.send(f'There were **{corrections}** correction(s) made')

@bot.command(name='check', help='Runs your text through LanguageTool and returns the result')
async def languagecheck(ctx, *args):
    if not args:
        await ctx.send('You didn\'t give me any text to parse!')
    else:
        text = ' '.join(args)
        print('{} arguments: {}'.format(len(args), ' '.join(args)))
        
        matches = tool.check(text)
        result = tool.correct(text)

        await ctx.send('**Corrected text:** ')
        await ctx.send(result)
        await ctx.send(f'There were **{len(matches)}** correction(s) made')


bot.run(TOKEN)