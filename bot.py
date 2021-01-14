import discord
import time
import datetime
import random
import typing
import os
import asyncio
import math
import json
from discord.ext import commands

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix= get_prefix)
token = 'bot token'
bot.remove_command('help')
start_time = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    print('-------') 
    print('Im Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Booting up...'))
    await asyncio.sleep(10)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Copper a simple Christmas bot | c!help | Happy New Year!"))
    await asyncio.sleep(5)
    channel = bot.get_channel(792461395886473248)
    for guild in bot.guilds:
        await channel.send(f"Connected to the server: **{guild.name}**({guild.id}) ✅")
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Command not found on {ctx.guild} | Command executed by {ctx.message.author}({ctx.message.author.id})")

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'c!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command(name='change_prefix')
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed=discord.Embed(title=f"Successfully set the custom prefix", description=f"For {ctx.guild} the prefix has been set to: `{prefix}` .If you want to change it again, you have to wait 10 seconds.", color=0xf7f3f3)
    await ctx.send(embed=embed)

@bot.command(name='stopbot')
@commands.is_owner()
async def stopbot(ctx):
    msg = await ctx.send("Loading...")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.send(f"Hey {ctx.message.author.mention}!I am now logging out :wave:")
    await asyncio.sleep(5)
    await bot.logout()

@bot.command(name='ping')
async def ping(ctx):
    msg = await ctx.send("Loading...")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.send(f"Copper Latency: {round(bot.latency * 1000)}ms")
    print(f'Bot ping is {round(bot.latency * 1000)}ms')

@bot.command(name='invite')
async def invite(ctx):
    invite_link = 'https://discord.com/api/oauth2/authorize?client_id=789918247830159400&permissions=8&scope=bot'
    await ctx.send(f"Use this invite link ({invite_link}) to invite me.")
    print(f"{ctx.message.author} wants to invite Sparky on {ctx.guild}")

@bot.command(name='about')
async def about(ctx):
    embed = discord.Embed(title= f'{bot.user.name}', color=0xf7f3f3)
    embed.add_field(name="**Developers:**", value="<@285130761860808704>", inline=False)
    embed.add_field(name="**Library:**", value="discord.py = 1.5.1", inline=False)
    embed.add_field(name="**Servers:**", value=f"{str(len(bot.guilds))}", inline=False)
    embed.add_field(name="**Commands:**", value=f"{str(len(bot.commands))}", inline=False)
    embed.add_field(name="**Ping:**", value=f"{round(bot.latency * 1000)}ms", inline=False)

    await ctx.send(embed=embed)
    print(f"{ctx.message.author} used command(about) on {ctx.guild}")

@bot.command(name='christmas_songs')
@commands.cooldown(1, 5, commands.BucketType.guild)
async def christmas_songs(ctx):
    clchsongs = "https://youtu.be/VaU6GR8OHNU"
    tpchsongs = "https://youtu.be/N51S9PLdQn8"
    embed=discord.Embed(title="Christmas Songs",description=f"Here are some Christmas songs you can listen to!", color=0xf7f3f3)
    embed.add_field(name='Classic Christmas Songs:',value=f"**[Click Here]({clchsongs})**",inline=False)
    embed.add_field(name='Trap Christmas Songs:',value=f"**[Click Here]({tpchsongs})**",inline=False)
    msg=await ctx.send(embed=embed)
    await msg.add_reaction("🎄")
    await msg.add_reaction("🎁")
    await msg.add_reaction("🎅")
    print(f"{ctx.message.author} wants to listen to some Christmas songs")

@bot.command(name='uptime')
async def uptime(ctx: commands.Context):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    msg = await ctx.send("Loading...")
    await asyncio.sleep(3)
    await msg.delete()
    await ctx.send(f"{bot.user.name} has been up for {uptime_stamp}")
    print(f"{bot.user.name} has been up for {uptime_stamp}")

@bot.command(name='say')
@commands.cooldown(1, 1, commands.BucketType.user)
@commands.has_permissions(send_tts_messages = True)
async def echo(ctx, *, content):
    await asyncio.sleep(1)
    if ctx.message.mention_everyone:
        embed=discord.Embed(title="Error", description="Your message mentions everyone and I will not send it!", color=0xf7f3f3)
        await ctx.send(embed=embed)
    else:
        await ctx.send(content)
        await ctx.message.delete()
    print(f"{ctx.message.author} sayed: {content} on {ctx.guild}")

@bot.command(name='send_gift')
@commands.has_permissions(send_tts_messages = True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def send_gift(ctx, member: discord.Member , *, gift):
    embed=discord.Embed(title="Hohoohoho!", description=f"{ctx.message.author.mention} gave you a Christmas present!", color=0xf7f3f3)
    embed.add_field(name="**Gift** received:", value=f"**{gift}**", inline=False)
    msg = await member.send(embed=embed)
    await msg.add_reaction("🎁")
    await asyncio.sleep(2)
    msg2 = await ctx.message.author.send(f"Your gift has been successfully sent!{member.mention} will be glad you gave him a present")
    await msg2.add_reaction("🎁")
    await asyncio.sleep(4)
    msg3 = await ctx.send("The gift has been sent!")
    await msg3.add_reaction("🎁")
    print(f"{ctx.message.author} gave {member} a gift ({gift})") 

@send_gift.error
async def send_gift_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="**Error**", description="Specify a member or gift", color=0xf7f3f3)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="**Error**", description="You do not have all the permissions to send a gift", color=0xf7f3f3)
        await ctx.send(embed=embed)

@bot.command(name='days')
async def days(ctx):
    delta = datetime.datetime(2020, 12, 25) - datetime.datetime.now()
    days = delta.days
    days_text = "days"
    if days == 1:
        days_text = "day"
    hours = math.floor(delta.seconds / 3600)
    minutes = math.ceil(delta.seconds / 60) - (hours * 60)
    minutes_text = "minutes"
    if minutes == 1:
        minutes_text = "minute"
    msg = await ctx.send("Now I look at the calendar and I will tell you how many days are left until Christmas")
    await msg.add_reaction('📅')
    await asyncio.sleep(3)
    await msg.delete()
    await ctx.send(f"Until Christmas there are: **{days}** {days_text} ,**{hours}** hours ,**{minutes}** {minutes_text}")
    print(f"{ctx.message.author} wants to know how many days are left until Christmas")

@bot.command(name='reputation_check')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def reputation_check(ctx):
    responses = ["right" , "bad "]
    msg = await ctx.send("Let me check which list you are on!This process can take about 5 seconds")
    await asyncio.sleep(4)
    await msg.delete()
    await ctx.send(f"{ctx.message.author.mention} you're on Santa's **{random.choice(responses)} list**!")

@bot.command(name='wishlist')
@commands.cooldown(1, 10, commands.BucketType.guild)
async def wishlist(ctx, *, question):
    await ctx.send("I told Santa what you want for Christmas and he told me he would bring you these Christmas presents.")
    await asyncio.sleep(5)
    message= f"{ctx.message.author} ({ctx.message.author.id}) wishes for christmas:: ** {question} **."
    channel = bot.get_channel(789929612884312064)
    await channel.send(message)

@bot.command(name='help')
async def helpcmd(ctx):
    message = '''
**🎁Christmas Commands:**
    `c!christmas_songs` - Some Christmas songs
    `c!send_gift @user#1234 gift` - Send a gift to a friend
    `c!days` - How many days are left until Christmas
    `c!reputation_check` - See if you're on Santa's good or bad list
    `c!wishlist the desired gifts` - The gifts you want for this Christmas that you want Santa to bring you
**⚙️Administrator Commands:**
    `c!change_prefix prefix` - Change Copper's prefix
**🗂Other:**
    `c!say message` - Say something using Copper
    `c!uptime` - Copper Uptime
    `c!ping` - Copper Latency
    `c!about` - Some information about Copper
    `c!invite` - Invite Copper to your Discord server
    '''
    await ctx.send(message)
    print(f"{ctx.message.author} wants to know my commands!")


bot.run(token)