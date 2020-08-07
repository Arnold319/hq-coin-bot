from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
import random
import requests
from discord.ext.commands import Bot
import discord
from discord.ext import commands
import random
import aiohttp
import csv
import json
import datetime
import os
import string
from unidecode import unidecode
import pymongo
from pymongo import MongoClient
import asyncio
client = pymongo.MongoClient("mongodb+srv://rohit123:9836124182@cluster0-9e2wk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.janina
database = db.user
lifebase = db.life
number_base = db.number
pending_base = db.pending
print(pending_base)
client = commands.Bot(command_prefix='+')
client.remove_command('help')
count = 0
#token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI2MDkzMjkzLCJ1c2VybmFtZSI6Im5hbWVzZEo0MjUiLCJhdmF0YXJVcmwiOiJodHRwczovL2Nkbi5wcm9kLmh5cGUuc3BhY2UvZGEvZ29sZC5wbmciLCJ0b2tlbiI6bnVsbCwicm9sZXMiOltdLCJjbGllbnQiOiJBbmRyb2lkLzEuMzkuMCIsImd1ZXN0SWQiOm51bGwsInYiOjEsImlhdCI6MTU2NTg2MDQxMSwiZXhwIjoxNTczNjM2NDExLCJpc3MiOiJoeXBlcXVpei8xIn0.EHLKDZpFsf-JIY_nPyWbtIo0HwPIuqWKYYdusQKC-o8'
value = 0
idk = 0    
hqusername = ["names"]
l1 = random.choice(string.ascii_letters)
l2 = random.choice(string.ascii_letters)
username = str(random.choice(hqusername))+str(l1)+str(l2)+str(random.randint(100,1000))

cwd = os.path.dirname(os.path.realpath(__file__))
api = HQApi()
c = ' '
#BOT_OWNER_ROLE = 'Coin Access'

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("I'm ready")
    while True:
    	await client.change_presence(game=discord.Game(type=1,name="with HQ COIN"))
    	await asyncio.sleep(5)
    	await client.change_presence(game=discord.Game(type=1,name="with +help"))
    	await asyncio.sleep(5)
    	await client.change_presence(game=discord.Game(type=1,name="with TRIVIA NATION"))
    	await asyncio.sleep(5)

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send_message(ctx.message.channel, 'you are on cool down')
@client.command(pass_context=True, no_pm=True)
async def hqlogin(ctx, message=None):
    global c
    global value
    x = ' '
    api = HQApi()
    tapauthor = ctx.message.author.mention
    user = ctx.message.author
    if message is None:
        return await ctx.send("**Wrong Input correct use : `+hqlogin <number with +1>`**")
    phonenumber = message
    print(phonenumber)
    await client.delete_message(ctx.message)
    if BOT_OWNER_ROLE in [role.name for role in ctx.message.author.roles]:
        try:
            x = api.send_code(phonenumber, "sms")
            print(x)
        except ApiResponseError:
            await ctx.send('invalid number please check your number')
        v = x['verificationId']
        abed=discord.Embed(title=f"Login in to Hq trivia", description="Help Command", color=0x73ee57 )
        abed.add_field(name=f"Code Sent", value='An four digit code has been sent to your number', inline=False)
        abed.add_field(name="guide:", value='To verify account type +code `<received otp>`', inline=False)
        abed.set_footer(text="",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRT4piNVysew5wAY3NGsxjxv-zDAoY4A7Ze9N79xThBuaHNVsnP")
        await ctx.send(embed=abed)

        global smscode
        smscode = None
        author = ctx.message.author
        def code_check(msg1):
            return msg1.content.lower().startswith('+code')
        smg = await client.wait_for_message(author=ctx.message.author, check=code_check)
        smscode = smg.content[len('+code'):].strip()
        print(smscode)
        try:
            value = int(smscode)
        except ApiResponseError:
            await ctx.send('invalid code please check your code')
        s = api.confirm_code(v, value)
        name = username
        print(name)
        referral = 'None'
        d = api.register(v, name, referral)
        token = d['authToken']
        c = d['username']
        await ctx.send(f"successfully added your number your profile next time just do `+hqplay {c}`")
        print(d)
        userid = user.id
        z = {'userid':userid,
                    'points':phonenumber,
                    'token':str(token),
                    'username':str(c)    
        }
        number_base.insert_one(z)
        print(z)
    else:
        await ctx.send('You don\'t have permission to use this command')
        

@client.command(pass_context=True, no_pm=True)
async def hqaccount(ctx):
    user = ctx.message.author
    id_list = []
    ref_list = []
    data = list(number_base.find())
    p = number_base.find()
    for i in data:
        id_list.append(i['userid'])
    if user.id in id_list:
        use = user.id
        p_list = number_base.find_one({'userid':use})['username']
        print(p_list)
        await ctx.send(f'your added profiles are {p_list}')
            
    else:
        await ctx.send('you didn\'t added any profile yet')
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    abed=discord.Embed(title=f"Hq Daily challenge", description="Help Command", color=0x73ee57 )
    abed.add_field(name=f"+hqlogin +1123445xxx", value='To add your <:hhhh:634462529921482762>account', inline=False)
    abed.add_field(name="+hqplay {refercode}", value='play hq Trivia daily challenge example and win 50<:hqcoin:637185641565782026> and 3000 points', inline=False)
    abed.add_field(name="+hqaccount", value='show you a list of account that are logged into the bot', inline=False)
    abed.set_footer(text="") 
    await ctx.send_message(author,embed=abed)
    await ctx.send('> **_HQ   DAILY   CHALLENGE_**\n> help command\n> **_CHECK   YOUR  DMs📨_**\n> Help command has been sent your dm||✅')

@client.command(pass_context=True, no_pm=True)
async def hqplay(ctx,refercode=None):
    if BOT_OWNER_ROLE in [role.name for role in ctx.message.author.roles]:
        global count
        global idk
        user = ctx.message.author.id
        print(refercode)
        embed=discord.Embed(title=f"HQ DAILY CHALLENGE", description="", color=0x73ee57 )
        embed.add_field(name="loading... It may take some second", value='🤔🤔', inline=False)
        embed.set_footer(text="Hq Daily challenge")
        x = await ctx.send(embed=embed)
        token_id = []
        ref_list = []
        
        data = list(number_base.find())
        p = number_base.find()
        
        for i in data:
            token_id.append(i['userid'])
            ref_list.append(i['username'])
            print(ref_list)
            print(token_id)
        if user in token_id and refercode in ref_list:
            use = user
            p_list = number_base.find_one({'userid':use,'username':refercode})['token']
            if p_list == 'NoneType':
                abed=discord.Embed(title=f"Hq Daily challenge", description="", color=0x73ee57 )
                abed.add_field(name=f"sorry ", value='its not your account', inline=False)
                await ctx.send(embed=abed)
            else:
                pass
            print(p_list)
            api = HQApi(p_list)
            
            
            
            try:
                offair_id = api.start_offair()['gameUuid']
                print(offair_id)
            except ApiResponseError:
                url = 'https://api-quiz.hype.space/shows/schedule?&type='
                headers = {

                'authority': 'api-quiz.hype.space',
                'accept': '*/*',
                'accept-encoding': 'br, gzip, deflate',
                'accept-language': 'en-us',
                'authorization': f'Bearer {p_list}',
                'user-agent': 'HQ-iOS/159 CFNetwork/975.0.3 Darwin/18.2.0',
                'x-hq-client': 'iOS/1.5.2 b159',
                'x-hq-country': 'en',
                'x-hq-device': 'iPhone11,6',
                'x-hq-deviceclass': 'phone',
                'x-hq-lang': 'en',
                'x-hq-stk': 'MQ==',
                'x-hq-timezone': 'America/New_York'
                    }
                gcheck = requests.get(url,headers=headers).json()
                embed=discord.Embed(title="Hq Daily challenge", description="", color=0x73ee57 )
                wait1 = gcheck['offairTrivia']['waitTimeMs']
                embed.add_field(name="Hq Daily challenge", value=f'❌ Game already played', inline=False)
                embed.add_field(name="you can't play more game daily challenge right now!!", value=f'use `+hqplay` after **{wait1}** milliseconds ', inline=False)
                embed.set_footer(text="",icon_url="https://cdn.discordapp.com/attachments/718400433844125767/740953567996805171/e2faa71710f3f99d507f2b42e2a87563.jpg")
                await client.edit_message(x,embed=embed)
                offair_id = api.get_schedule()['offairTrivia']['games'][0]['gameUuid']
                print(offair_id)
                
                
            embed=discord.Embed(title=f"HQ DAILY CHALLENGE", description="", color=0x73ee57 )
            embed.add_field(name="Starting playing", value='waiting..', inline=False)
            embed.set_footer(text="Hq Daily challenge")
            v = await client.edit_message(x,embed=embed)
            await asyncio.sleep(3) 
            while True:
                offair = api.offair_trivia(offair_id)
                print("Question {0}/{1}".format(offair['question']['questionNumber'], offair['questionCount']))
                print(offair['question']['question'])
                
                for answer in offair['question']['answers']:
                    print('{0}. {1}'.format(answer['offairAnswerId'], answer['text']))
                    answers = [unidecode(answer["text"]) for answer in offair['question']["answers"]] 
                lol = random.randint(0,3)
                q= offair['question']['question']
                    #print(base)
                url = 'https://www.dl.dropboxusercontent.com/s/0ea433zcpljtv3j/sitejson.json?dl=0'
                r = requests.get(url)
                a = json.loads(r.text)
                base = {'ques':[],
                    'right':[]
                    }
                for i in a["questionData"]:
                    c = i['question']
                    ok = i['answerCounts']
                    base['ques'].append(c)
                    base['right'].append(ok)
                    basa = base['right']
                if q in base['ques']:
                    on = base['ques'].index(q)
                    print(on)
                    print('yes found in database')
                    x = base={'ques':q}
                    print(x)
                    ans = basa[on]
                    x = 0
                    for i in ans:
                        print(i)
                        if i['correct']==True:
                            try:
                                answerdict=answers
                                cor = i['answer']
                                x = answerdict.index(cor)
                                print(x)
                            except ValueError:
                                lol = random.randint(0,3)
                                answer = api.send_offair_answer(offair_id, offair['question']['answers'][lol -1]['offairAnswerId'])
                            answer = api.send_offair_answer(offair_id, offair['question']['answers'][x]['offairAnswerId'])
                            ree = answer['seasonXp']['currentPoints']
                            pe = answer['pointsEarned']
                            qm = answer['questionNumber']
                            print(ree)
                            print('You got it right: ' + str(answer['youGotItRight']))
                            if answer['youGotItRight']== True:
                                count += 1
                else:
                    print('nope not in database')
                    lol = random.randint(0,3)
                    answer = api.send_offair_answer(offair_id, offair['question']['answers'][lol -1]['offairAnswerId'])
                    el = HQApi(token=p_list)
                    a = el.get_users_me()
                    for i in a['seasonXp']:
                        idk = i['currentPoints']
                    pe = answer['pointsEarned']
                    qm = answer['questionNumber']
                    print('You got it right: ' + str(answer['youGotItRight']))
                    if answer['youGotItRight']== True:
                        count += 1
                abed=discord.Embed(title=f"Hq Daily challenge", description=f"{c}", color=0x73ee57 )
                abed.add_field(name=f"<:hhhh:634462529921482762> Username:- {refercode}", value=f'<:hhhh:634462529921482762> Point earned{pe}\n<:hhhh:634462529921482762> Total Points:-{idk}', inline=False)
                abed.add_field(name=f"Question Correct {count}/{offair['questionCount']}", value='\u200b', inline=False)
                abed.set_footer(text="Hq Daily challenges playing now")
                e = await client.edit_message(v,embed=abed)
       
                if answer['gameSummary']:
                    print(answer['gameSummary'])
                    print('Game ended')
                    print('Earned:')
                    api = HQApi(token=p_list)
                    a = api.get_users_me()
                    coin = a['coins']
                    print('Coins: ' + str(answer['gameSummary']['coinsEarned']))
                    print('Points: ' + str(answer['gameSummary']['pointsEarned']))
                    embed=discord.Embed(title=f"Hq Daily challenge", description="", color=0x73ee57 )
                    embed.add_field(name=f"✅HQ DAILY CHALLENGE PLAYED {refercode}", value=f"<:disco:634462418344345600>  Discord user:-<@{user}>", inline=False)
                    embed.add_field(name=f"<:hhhh:634462529921482762> Username:-{refercode}", value=f"**<:hhhh:634462529921482762>  Question Correct:-{count}/{offair['questionCount']}\n<:ccccc:634464030446190602> Earned Coins:-{str(answer['gameSummary']['coinsEarned'])}\n<:hhhh:634462529921482762>  Earned Points:-{str(answer['gameSummary']['pointsEarned'])}**", inline=False)                
                    embed.add_field(name=f"<:hhhh:634462529921482762> Total Points:-{ree}", value=f"**<:hqcoin:637185641565782026> Total Coins:-{coin}**", inline=False)
                    embed.set_footer(text="")
                    await client.edit_message(e,embed=embed)
                    count = 0
                    break
            
            else:
                await ctx.send('you didn\'t added any number')
    else:
        await ctx.send('You have no permission')
            
client.run("NzQwMDk2ODg5MjMxMjQ1MzUy.XykC8A.bK0nLhDsNyqyolAGs1wgkTFKl0c")
