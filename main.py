import os
import logging
import discord
from discord.ext import commands, tasks
import json
import requests
import time
from bot_token import token


#Discord ID info
activity = discord.Game(name="with your feelings")
author_id = '892999941146963969'
channel_id = 923432498925547531

#Variables
url = 'https://qlbbl-api.net'
Helluva = 0

#Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#Bot info
bot = commands.Bot(
	command_prefix="~",  # Change to desired prefix
	case_insensitive=True, # Commands aren't case-sensitive
    activity=activity,
    status=discord.Status.idle 
)

#Author ID
bot.author_id = author_id  # Change to your discord id!!!


#Bot Ready
@bot.event 
async def on_ready():  # When the bot is ready
    print(f"{bot.user} Started.")
 
#COMMANDS

#Test
@bot.command(name='test', help='Tests the bot.')
async def test(ctx, *, arg):
  print(arg)
  await ctx.send(arg)

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Error: Something went wrong.')


#Hazbin Image
@bot.command(name='hazbin', help='Gets a random gif or image from the qlbbl-api.')
async def hazbin(ctx):

    response = requests.get(f"{url}/v1/hazbin/gif/random")
    r = json.loads(response.text)

    await ctx.send(r)

@hazbin.error
async def hazbin_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Error: Something went wrong.')


#Qlbbl-Api
@bot.command(name='qlbblapi', help='Fetch from the qlbbl-api.')
async def qlbblapi(ctx, *args):

    response = requests.get('{}/{}'.format(url, '/'.join(args)))
    response_value = response
    print(response)
    if response.status_code == 200:
        r = json.loads(response.text)
        f = open("response.txt", "w")
        f.write(f'{json.dumps(r, indent=4)}')
        f.close()
        await ctx.send(f'{response}\n', file=discord.File('response.txt'))
        os.remove("response.txt")
    else:
        await ctx.send('Error: Bad request.')

@qlbblapi.error
async def qlbblapi_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Error: Something went wrong.')


#TASKS

#Helluva Boss Loop
@tasks.loop(seconds=86400)
async def called_once_a_day():
    message_channel = bot.get_channel(channel_id)
    if Helluva == 0:
        await message_channel.send("__Is part 2 of the Helluva Boss finale out yet?__")
        time.sleep(3)
        await message_channel.send('https://i.imgur.com/3sARn4H.jpeg')
    elif Helluva == 1:
        await message_channel.send("__Is part 2 of the Helluva Boss finale out yet?__")
        time.sleep(3)
        await message_channel.send('YES! \n https://tenor.com/view/oh-yeah-mochi-peach-cat-corean-gif-24678746') 

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Sent Daily Message")





#boiler plate
if __name__ == '__main__':
  pass


#main functions
#called_once_a_day.start()
bot.run(token)  # Starts the bot

