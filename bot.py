# bot code here
import discord
from discord.ext import commands
from discord.ext.commands.converter import InviteConverter
from discord.ext.commands.core import check
from discord.utils import get
import requests
import json
import asyncio

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game('?verify <scratchusername>'))

@client.command()
async def verify(ctx, username):
    r = requests.put('https://scratchverifier.ddns.net/verify/' + username, auth=('28588350', '0b855b91d3bfbe6635195d4edf9bf147b3f7201d78a8786c7e8ddf2273959bb0'))
    obj = json.loads(r.content)
    comment_code = obj["code"]
    embed = discord.Embed(
        description = 'React with ✅ to continue, and ❌ to cancel.',
        color = discord.Color.green())

    embed.set_footer(text='Scratch Verifier Discord Bot is a project by SharkBaitBilly#5270')
    embed.set_author(name='Verify A Scratch User',
    icon_url='https://u.cubeupload.com/ajsya/scratchverifyer.png')
    embed.add_field(name='Comment the following code on your profile!', value=comment_code, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction(emoji='\U00002705')
    await message.add_reaction(emoji='\U0000274C')
    def check(reaction, user):
        return str(reaction.emoji) in ['✅', '❌'] and user != client.user
    try:
        reaction, user = await client.wait_for('reaction_add', check=check, timeout=120.0)
    except asyncio.TimeoutError:
        await ctx.send("User Verification Cancled")
    else:
        if str(reaction.emoji) == '✅':
            r = requests.post('https://scratchverifier.ddns.net/verify/' + username, auth=('28588350', '0b855b91d3bfbe6635195d4edf9bf147b3f7201d78a8786c7e8ddf2273959bb0'))
            if r.status_code == 204:
                await ctx.author.edit(nick=username, reason='Verified with Scratch using ?verify <username>')
                role = get(ctx.author.guild.roles, name='Verified')
                await ctx.author.add_roles(role, reason='Verified with Scratch using ?verify <username>')
                await ctx.send('Verified!')
                print('User "' + username + '" was verified!')
            else:
                await ctx.send('Error while verifying!')

        if str(reaction.emoji) == '❌':
            await ctx.send("User Verification Canceled")

@client.command()
async def profile(ctx, username):
    r = requests.get('https://scratchdb.lefty.one/v2/user/info/' + username)

    obj = json.loads(r.content)
    id = obj["id"]
    userFollowers = obj["followers"]
    userBio = obj["bio"]
    userWork = obj["work"]
    icon = "https://cdn2.scratch.mit.edu/get_image/user/" + str(id) + "_90x90.png"
    embed = discord.Embed(
        description = username + ' on Scratch!',
        color = discord.Color.orange())

    embed.set_footer(text='Scratch Verifier Discord Bot is a project by SharkBaitBilly#5270')
    embed.set_author(name=username, icon_url=icon,)
    embed.set_thumbnail(url=icon)
    embed.add_field(name='About Me', value=userBio, inline=False)
    embed.add_field(name="What I'm working On", value=userWork, inline=False)
    embed.add_field(name='Followers', value=userFollowers, inline=False)
    message = await ctx.send(embed=embed)

@client.command()
async def scratchstats(ctx, username):
    r = requests.get('https://scratchdb.lefty.one/v2/user/info/' + username)

    obj = json.loads(r.content)
    id = obj["id"]
    a = obj["statistics"]
    userFollowers = obj["followers"]
    userFollowing = obj["following"]
    userViews = a["views"]
    userLoves = a["loves"]
    userFavorites = a["favorites"]
    userComments = a["comments"]
    
    icon = str("https://cdn2.scratch.mit.edu/get_image/user/" + str(id) + "_90x90.png")

    embed = discord.Embed(
        description = username + "'s Scratch Stats",
        color = discord.Color.orange())

    embed.set_footer(text='Scratch Verifier Discord Bot is a project by SharkBaitBilly#5270')
    embed.set_author(name=username,
    icon_url=icon)
    embed.add_field(name='Followers', value=userFollowers, inline=False)
    embed.add_field(name='Following', value=userFollowing, inline=True)
    embed.add_field(name='Total Views', value=userViews, inline=False)
    embed.add_field(name='Total Comments', value=userComments, inline=True)
    embed.add_field(name='Total Loves', value=userLoves, inline=False)
    embed.add_field(name='Total Favorites', value=userFavorites, inline=True)
    message = await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        color = discord.Color.orange())

    embed.set_footer(text='Scratch Verifier Discord Bot is a project by SharkBaitBilly#5270')
    embed.set_author(name='Scratch Verifier Discord Bot',
    icon_url='https://u.cubeupload.com/ajsya/scratchverifyer.png')
    embed.add_field(name='Invite to your server!', value='https://discord.com/oauth2/authorize?client_id=736356485042274304&permissions=1543776320&scope=bot', inline=False)
    embed.add_field(name='Join our Support Server!', value='https://discord.gg/ZQHYX93PX5', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def credits(ctx):
    embed = discord.Embed(
        title = 'Credits',
        description = 'Without these people Scratch Verifier Discord Bot would not be possible',
        color = discord.Color.orange())

    embed.set_thumbnail(url='https://u.cubeupload.com/ajsya/scratchverifyer.png')
    embed.set_author(name='Scratch Verifier Discord Bot',
    icon_url='https://u.cubeupload.com/ajsya/scratchverifyer.png')
    embed.add_field(name='API Library', value='https://github.com/ScratchVerifier/ScratchVerifier', inline=False)
    embed.add_field(name='SharkBaitBilly#5270', value="Head Developer", inline=False)
    embed.add_field(name='Semisol#0001', value="Library Help", inline=False)
    await ctx.send(embed=embed)

TOKEN = "NzM2MzU2NDg1MDQyMjc0MzA0.Xxtnag.amczYDbe7xsFfCr-sPYZ97KA95g"
client.run(TOKEN)
