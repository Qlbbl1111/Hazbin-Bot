import os
import discord
from discord.ext import commands, tasks
import json
import requests
import time
import token

bot_token = token
author_id = '892999941146963969'
api_key= ''
img = 'https://i.imgur.com/kPLPAJs.jpg'
activity = discord.Game(name="with your feelings")
channel_id = 923432498925547531

#Command prefix.
bot = commands.Bot(
	command_prefix="~",  # Change to desired prefix
	case_insensitive=True, # Commands aren't case-sensitive
    activity=activity,
    status=discord.Status.idle 
)

bot.author_id = author_id  # Change to your discord id!!!


@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)
 


#Test
@bot.command(name='test', help='Tests the bot.')
async def test(ctx, *, arg):
  print(arg)
  await ctx.send(arg)

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Error: Something went wrong.')



#Message 1
@tasks.loop(seconds=86400)
async def called_once_a_day():
  message_channel = bot.get_channel(channel_id)
  await message_channel.send("__Is the new episode of Helluva Boss out yet?__")
  time.sleep(3)
  await message_channel.send(img)

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


if __name__ == '__main__':
  pass


called_once_a_day.start()

bot.run(bot_token)  # Starts the bot