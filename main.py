from dataclasses import dataclass
import discord 
import requests
import asyncio

from bs4 import BeautifulSoup
from discord.ext import commands


checked_num = 0
notify_keywords = ['질문', '뉴비', '?', '도움']



header = {'User-Agent' : ''}

minor_base_url = 'https://gall.dcinside.com/mgallery/board/lists'
minor_ids = {'id':'game_dev'}

datastr = ""

client = discord.Client()


async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(채널번호)  # channel ID goes here
    print("Start Task")
    while not client.is_closed():
        global datastr
        datastr = ''
        resp = requests.get(minor_base_url,params=minor_ids, headers=header)
        ExtractNewArticle(resp)

        print("data : "+datastr)
        if(datastr != ''):
            await channel.send(datastr)
        await asyncio.sleep(10)  # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in')

def ExtractNewArticle(resp):
    global datastr
    global checked_num

    init_mode = checked_num == 0
    soup = BeautifulSoup(resp.content, 'html.parser')
    contents = soup.find('tbody').find_all('tr')


    for content in contents:
        is_ask_article = False
        gall_subject = content.find('td',class_='gall_subject').text
        
        if(gall_subject == '공지' or gall_subject == '설문'):
            continue

        gall_num = int(content.find('td', class_= 'gall_num').text)
        
        if(gall_num <= checked_num and init_mode == False):
            break
        checked_num = gall_num
        article_title = content.find('a').text

        if(gall_subject == '💬질문'):
            is_ask_article = True
        else:
            for notiword in notify_keywords:
                if(article_title.find(notiword) != -1):
                    is_ask_article = True
                    break
        
        if(is_ask_article):
            datastr += article_title + ' : '
            datastr += minor_base_url + '&no='
            datastr += str(gall_num)
            datastr += '\n'

    
    return
if __name__ == '__main__':
    client.loop.create_task(my_background_task())
    client.run(봇토큰)